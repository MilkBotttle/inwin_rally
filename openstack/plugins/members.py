from rally.task import validation
from rally.task import types

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.octavia import utils as octavia_utils
from rally_openstack.scenarios.nova import utils as nova_utils


"""Scenarios for Octavia Loadbalancer member."""


@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.list_members",
                    platform="openstack")
class ListMembers(octavia_utils.OctaviaBase):

    def run(self, protocol="HTTP", pool_id=None):
        if pool_id:
            self.octavia.member_list(pool_id)
        else:
            subnets = []
            loadbalancers = []
            networks = self.context.get("tenant", {}).get("networks", [])
            for network in networks:
                subnets.extend(network.get("subnets", []))
            for subnet_id in subnets:
                lb = self.octavia.load_balancer_create(subnet_id)
                loadbalancers.append(lb)
            for loadbalancer in loadbalancers:
                self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
                pool = self.octavia.pool_create(
                    lb_id=loadbalancer["id"],
                    protocol=protocol, lb_algorithm="ROUND_ROBIN")
                self.octavia.member_list(pool["id"])

@types.convert(image={"type": "glance_image"},
               flavor={"type": "nova_flavor"})
@validation.add("image_valid_on_flavor", flavor_param="flavor",
                image_param="image", fail_on_404_image=False)
@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NOVA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia","nova"]},
                    name="Octavia.create_member_and_delete",
                    platform="openstack")
class CreateMemberAndDelete(octavia_utils.OctaviaBase, nova_utils.NovaScenario):
    def run(self, flavor, image, protocol="HTTP",
                                 protocol_port=80,
                                 lb_algorithm="ROUND_ROBIN"):
        networks = self.context.get("tenant", {}).get("networks", [])
        nic = {
            "nics": [
                {"net-id": networks[0]["id"]}
            ]
        }
        server = self._boot_server(image, flavor, nic)
        subnet_id = networks[0]["subnets"][0]
        lb = self.octavia.load_balancer_create(subnet_id)
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        pool = self.octavia.pool_create(lb_id=lb["id"],
                                        protocol=protocol,
                                        lb_algorithm=lb_algorithm)
        member_args = {
            "protocol_port": protocol_port,
            "name": server.name,
            "address": server.interface_list()[0].fixed_ips[0]["ip_address"]
        }
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        member = self.octavia.member_create(pool["id"], json={"member": member_args})
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        self.octavia.member_delete(pool_id=pool["id"],member_id=member["member"]["id"])


@types.convert(image={"type": "glance_image"},
               flavor={"type": "nova_flavor"})
@validation.add("image_valid_on_flavor", flavor_param="flavor",
                image_param="image", fail_on_404_image=False)
@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NOVA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia","nova"]},
                    name="Octavia.create_member_and_update",
                    platform="openstack")
class CreateMemberAndUpdate(octavia_utils.OctaviaBase, nova_utils.NovaScenario):
    def run(self, flavor, image, protocol="HTTP",
                                 protocol_port=80,
                                 update_protol_port=8080,
                                 lb_algorithm="ROUND_ROBIN"):
        subnets = []
        loadbalancers = []
        networks = self.context.get("tenant", {}).get("networks", [])
        nic = {
            "nics": [
                {"net-id": networks[0]["id"]}
            ]
        }
        server = self._boot_server(image, flavor, nic)
        subnet_id = networks[0]["subnets"][0]
        lb = self.octavia.load_balancer_create(subnet_id)
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        pool = self.octavia.pool_create(lb_id=lb["id"],
                                        protocol=protocol,
                                        lb_algorithm=lb_algorithm)
        member_args = {
            "protocol_port": protocol_port,
            "name": server.name,
            "address": server.interface_list()[0].fixed_ips[0]["ip_address"]
        }
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        member = self.octavia.member_create(pool["id"], json={"member": member_args})
        self.octavia.wait_for_loadbalancer_prov_status(lb)
        set_args = {
            "monitor_port": update_protol_port
        }
        self.octavia.member_set(pool_id=pool["id"], member_id=member["member"]["id"],
                                json={"member": set_args})


