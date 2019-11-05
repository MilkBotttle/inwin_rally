from rally.task import validation

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.octavia import utils as octavia_utils

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.healthmonitors_list",
                    platform="openstack")
class HealthMonitorsList(octavia_utils.OctaviaBase):
    def run(self):
        self.octavia.health_monitor_list()

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.create_and_delete_healthmonitors",
                    platform="openstack")
class CreateAndDeleteHealthMonitors(octavia_utils.OctaviaBase):
    def run(self, protocol="HTTP", monitor_type="PING", lb_algorithm="ROUND_ROBIN"):
        subnets = []
        loadbalancers = []
        pools = []
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
            pools.append(pool)
        for p in pools:
            monitor_args = {
                "pool_id" : p["id"],
                "delay": 1,
                "timeout": 30,
                "type": monitor_type.upper(),
                "max_retries": 10
            }
            hm = self.octavia.health_monitor_create(json={"healthmonitor": monitor_args})
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            self.octavia.health_monitor_delete(hm["healthmonitor"]["id"])

@validation.add("required_services", services=[consts.Service.OCTAVIA])
@validation.add("required_platform", platform="openstack", users=True)
@validation.add("required_contexts", contexts=["network"])
@scenario.configure(context={"cleanup@openstack": ["octavia"]},
                    name="Octavia.create_and_update_healthmonitors",
                    platform="openstack")
class CreateAndUpdateHealthMonitors(octavia_utils.OctaviaBase):
    def run(self, protocol="HTTP", monitor_type="PING", lb_algorithm="ROUND_ROBIN"):
        subnets = []
        loadbalancers = []
        pools = []
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
            pools.append(pool)
        for p in pools:
            monitor_args = {
                "pool_id" : p["id"],
                "delay": 1,
                "timeout": 30,
                "type": monitor_type.upper(),
                "max_retries": 10
            }
            hm = self.octavia.health_monitor_create(json={"healthmonitor": monitor_args})
            self.octavia.wait_for_loadbalancer_prov_status(loadbalancer)
            set_args = {
                "delay": 10,
                "timeout": 60
            }
            self.octavia.health_monitor_set(health_monitor_id=hm["healthmonitor"]["id"],
                                            json={"healthmonitor": set_args})
