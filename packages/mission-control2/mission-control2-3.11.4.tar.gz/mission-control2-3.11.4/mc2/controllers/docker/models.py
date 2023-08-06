import json

from django.db import models
from django.conf import settings

from mc2.controllers.base.models import Controller, EnvVariable, MarathonLabel


def marathon_lb_domains(domains):
    """
    marathon-lb takes comma-separated domain names for its HAPROXY_{n}_VHOST
    labels. Convert our space-separated domains to that form.
    """
    return ",".join(domains.split())


def traefik_domains(domains):
    """
    Create the traefik.frontend.rule label from the string of domains we use
    for templated Nginx/marathon-lb.
    """
    if not domains.strip():
        return ''

    return "Host: %s" % (", ".join(domains.split()),)


class DockerController(Controller):
    docker_image = models.CharField(max_length=256)
    marathon_health_check_path = models.CharField(
        max_length=255, blank=True, null=True)
    port = models.PositiveIntegerField(default=0, blank=True, null=True)
    domain_urls = models.TextField(max_length=8000, default="")
    external_visibility = models.BooleanField(default=True)
    volume_needed = models.BooleanField(default=False)
    volume_path = models.CharField(max_length=255, blank=True, null=True)

    def get_marathon_app_data(self):
        app_data = super(DockerController, self).get_marathon_app_data()
        docker_dict = {
            "image": self.docker_image,
            "forcePullImage": True,
            "network": "BRIDGE",
        }

        if self.port:
            docker_dict.update({
                "portMappings": [{"containerPort": self.port, "hostPort": 0}]
            })

        parameters_dict = [{"key": "memory-swappiness", "value": "0"}]
        if self.volume_needed:
            parameters_dict.append({"key": "volume-driver", "value": "xylem"})
            parameters_dict.append({
                "key": "volume",
                "value": "%(app_id)s_media:%(path)s" % {
                    'app_id': self.app_id,
                    'path':
                        self.volume_path or
                        settings.MARATHON_DEFAULT_VOLUME_PATH}})

        if parameters_dict:
            docker_dict.update({"parameters": parameters_dict})

        domains = "%(generic_domain)s %(custom)s" % {
            'generic_domain': self.get_generic_domain(),
            'custom': self.domain_urls
        }
        domains = domains.strip()

        service_labels = self.get_default_app_labels()
        service_labels.update({
            "HAPROXY_GROUP": "internal",
            "HAPROXY_0_VHOST": marathon_lb_domains(domains),
        })

        if self.external_visibility:
            service_labels.update({
                "domain": domains,
                "HAPROXY_GROUP": "external",
                "traefik.frontend.rule": traefik_domains(domains),
            })

        # Update custom labels
        if self.label_variables.exists():
            for label in self.label_variables.all():
                service_labels[label.name] = label.value

        app_data.update({
            "labels": service_labels,
            "container": {
                "type": "DOCKER",
                "docker": docker_dict
            },
            "backoffSeconds": settings.MESOS_DEFAULT_BACKOFF_SECONDS,
            "backoffFactor": settings.MESOS_DEFAULT_BACKOFF_FACTOR,
        })

        if self.marathon_health_check_path and self.port:
            app_data.update({
                "ports": [0],
                "healthChecks": [{
                    "gracePeriodSeconds":
                        int(settings.MESOS_DEFAULT_GRACE_PERIOD_SECONDS),
                    "intervalSeconds":
                        int(settings.MESOS_DEFAULT_INTERVAL_SECONDS),
                    "maxConsecutiveFailures": 3,
                    "path": self.marathon_health_check_path,
                    "portIndex": 0,
                    "protocol": "HTTP",
                    "timeoutSeconds":
                        int(settings.MESOS_DEFAULT_TIMEOUT_SECONDS),
                }]
            })

        return app_data

    @classmethod
    def from_marathon_app_data(cls, owner, org, app_data, name=None):
        """
        Create a new model from the given Marathon app data.

        NOTE: This is tested with the output of `get_marathon_app_data()`
        above, so it may not correctly handle arbitrary fields.
        """
        # Round-trip through JSON so we:
        # (a) know that everything's valid JSON
        # (b) get our own copy that we can modify without changing our input.
        app_data = json.loads(json.dumps(app_data))

        docker_dict = app_data["container"].pop("docker")
        args = {
            "slug": app_data.pop("id"),
            "marathon_cpus": app_data.pop("cpus"),
            "marathon_mem": app_data.pop("mem"),
            "marathon_instances": app_data.pop("instances", 1),
            "marathon_cmd": app_data.pop("cmd", ""),
            "docker_image": docker_dict.pop("image"),
        }
        # TODO: Better error:
        assert docker_dict.pop("network") == "BRIDGE"
        assert docker_dict.pop("forcePullImage", True) is True
        assert app_data.pop("container") == {"type": "DOCKER"}

        if "portMappings" in docker_dict:
            # TODO: Better error:
            assert len(docker_dict["portMappings"]) == 1
            args["port"] = docker_dict.pop("portMappings")[0]["containerPort"]

        for param in docker_dict.pop("parameters", []):
            if param["key"] == "volume":
                args["volume_needed"] = True
                args["volume_path"] = param["value"].split(":", 1)[1]

        labels = []

        gen_domain = (u"%s.%s" % (args["slug"], settings.HUB_DOMAIN)).strip()
        for k, v in app_data.pop("labels").items():
            if k == "name":
                args["name"] = v
            elif k == "domain":
                args["domain_urls"] = u" ".join(
                    [d for d in v.split(u" ") if d != gen_domain])
            elif k == 'HAPROXY_GROUP' and v == 'internal':
                args["external_visibility"] = False
                labels.append({"name": k, "value": v})
            else:
                labels.append({"name": k, "value": v})

        if "healthChecks" in app_data:
            # TODO: Validate the rest of the health check data.
            # TODO: Better errors:
            assert app_data.pop("ports", [0]) == [0]
            hc = app_data.pop("healthChecks")
            assert len(hc) == 1
            args["marathon_health_check_path"] = hc[0]["path"]

        if name is not None:
            args["name"] = name

        self = cls.objects.create(owner=owner, organization=org, **args)

        for label in labels:
            MarathonLabel.objects.create(controller=self, **label)

        for key, value in app_data.pop("env", {}).items():
            EnvVariable.objects.create(controller=self, key=key, value=value)

        for name, link in app_data.pop("link", {}).items():
            EnvVariable.objects.create(controller=self, name=name, link=link)

        # TODO: Better errors:
        # NOTE: Popping these backoffFactor and backoffSeconds because they're
        #       deployment defaults at the moment, not app specific ones.
        app_data.pop('backoffFactor', None)
        app_data.pop('backoffSeconds', None)
        assert docker_dict == {}
        assert app_data == {}

        return self

    def to_dict(self):
        data = super(DockerController, self).to_dict()
        data.update({
            'port': self.port,
            'marathon_health_check_path': self.marathon_health_check_path
        })
        return data

    def get_generic_domain(self):
        return '%(app_id)s.%(hub)s' % {
            'app_id': self.app_id,
            'hub': settings.HUB_DOMAIN
        }
