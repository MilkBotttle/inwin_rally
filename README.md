# Rally container docker file, and tasks.
## Prepare env for test
1. create a rally test user
```
openstack project create rally_test
openstack user create rally_test --password rally --project rally_test
openstack role add --user rally_test --project rally_test admin
```
2. create env for rally 
3. check env
## Run task
1. Edit `task_args.yaml`
2. Run Task `rally task start --task task.yaml`

