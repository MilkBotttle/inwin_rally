from rally.task import validation

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.octavia import utils as octavia_utils

"""Scenarios for Octavia Loadbalancer."""


@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.list_listeners",
                    platform="openstack")
class ListListeners(octavia_utils.OctaviaBase):
    """ List loadbalancer listeners. """
    def run(self):
       self.octavia.listener_list()

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.create_and_list_listeners",
                    platform="openstack")
class CreateAndListListeners(octavia_utils.OctaviaBase):
    def run(self, protocol_port=80, protocol="TCP"):
        subnets = []
        loadbalancers = []
        listeners = []
        networks = self.context.get("tenant", {}).get("networks", [])
        for network in networks:
            subnets.extend(network.get("subnets", []))
        for subnet_id in subnets:
            lb = self.octavia.load_balancer_create(subnet_id)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            args = {
                "name": self.generate_random_name(),
                "loadbalancer_id": loadbalancer["id"],
                "protocol": protocol,
                "protocol_port": protocol_port
            }
            ls = self.octavia.listener_create(json={"listener":args})
            listeners.append(ls)
        self.octavia.listener_list()

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.create_and_delete_listeners",
                    platform="openstack")
class CreateAndDeleteListeners(octavia_utils.OctaviaBase):
    def run(self, protocol_port=80, protocol="TCP"):
        subnets = []
        loadbalancers = []
        listeners = []
        networks = self.context.get("tenant", {}).get("networks", [])
        for network in networks:
            subnets.extend(network.get("subnets", []))
        for subnet_id in subnets:
            lb = self.octavia.load_balancer_create(subnet_id)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            args = {
                "name": self.generate_random_name(),
                "loadbalancer_id": loadbalancer["id"],
                "protocol": protocol,
                "protocol_port": protocol_port
            }
            ls = self.octavia.listener_create(json={"listener":args})
            listeners.append(ls)
        for listener in listeners:
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            self.octavia.listener_delete(listener["listener"]["id"])

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.create_and_update_listeners",
                    platform="openstack")
class CreateAndUpdateListeners(octavia_utils.OctaviaBase):
    def run(self, protocol_port=80, protocol="TCP"):
        subnets = []
        loadbalancers = []
        listeners = []
        networks = self.context.get("tenant", {}).get("networks", [])
        for network in networks:
            subnets.extend(network.get("subnets", []))
        for subnet_id in subnets:
            lb = self.octavia.load_balancer_create(subnet_id)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            args = {
                "name": self.generate_random_name(),
                "loadbalancer_id": loadbalancer["id"],
                "protocol": protocol,
                "protocol_port": protocol_port
            }
            ls = self.octavia.listener_create(json={"listener":args})
            listeners.append(ls)
            for listener in listeners:
                self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
                listener_args = {
                    "name": self.generate_random_name()
                }
                self.octavia.listener_set(
                    listener["listener"]["id"],
                    json={"listener": listener_args})
