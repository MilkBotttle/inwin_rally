# Rally container docker file, and tasks.
## Prepare env for test

1. Create a user in openstack for rally test
```
openstack project create rally_test
openstack user create rally_test --password rally --project rally_test
openstack role add --user rally_test --project rally_test admin
```

2. Create external network and private network and record their id
Create external network
> If use existing external skip this
```
openstack network create --share --provider-physical-network physnet1 \
  --provider-network-type flat --external rally_ext
openstack subnet create --subnet-range 203.0.113.0/24 --gateway 203.0.113.1 \
  --network rally_ext --allocation-pool start=203.0.113.11,end=203.0.113.250 \
  --no-dhcp --dns-nameserver 8.8.4.4 raly_ext_v4
```

Create private network 
```
openstack network create rally_pri
openstack subnet create --subnet-range 100.1.0.0/25 --network rally_pri
```
3. Download image for test 
[cirros download](http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img)

4. Create a rally environment file `env.yaml`
```
---
openstack:
  auth_url: http://10.168.1.199:35357/v3
  endpoint_type: internal
  region_name: RegionOne
  admin:
    username: admin
    password: openstack
    tenant_name: admin
  users:
    - username: cameron
      password: cameron
      tenant_name: cameron

```
5. Create env
```
rally env create --spec env.yaml --name openstack
```

6. Check env
```
rally env check 
```
## Run task
Edit task args and run.
Read [doc](openstack/README.rst)
