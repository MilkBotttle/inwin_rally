from rally.task import validation
from rally.task import types

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.nova import utils as nova_utils


@types.convert(image={"type": "glance_image"},
               flavor={"type": "nova_flavor"})
@validation.add("image_valid_on_flavor", flavor_param="flavor",
                image_param="image", fail_on_404_image=False)
@validation.add("required_services", services=[consts.Service.NOVA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["nova"]},
                    name="Nova.create_server_on_all_host",
                    platform="openstack")
class CreateServerOnAllHost(nova_utils.NovaScenario):
    def run(self, flavor, image, count=None):
        aggregates= self._list_aggregates()
        networks = self.context.get("tenant", {}).get("networks", [])
        nic = {
            "nics": [
                {"net-id": networks[0]["id"]}
            ]
        }

        for s in self.clients("nova").services.list(binary='nova-compute'):
            if s.status == 'enabled' and s.state == 'up':
                args = {
                    "avabilability_zone": s.zone + ":" + s.host
                }
                self._boot_server(image, flavor, nic, json={"server": args})
