============================
OpenStack Certification Task
============================


How To Validate & Run Task
--------------------------

To validate task with your own parameters run:

.. code-block:: console

  $ rally task validate task.yaml --task-args-file task_arguments.yaml


To start task with your own parameters run:

.. code-block:: console

  $ rally task start task.yaml --task-args-file task_arguments.yaml


Task Arguments
--------------

File task_arguments.yaml contains all task options:

+------------------------+----------------------------------------------------+
| Name                   | Description                                        |
+========================+====================================================+
| smoke                  | Dry run without load from 1 user                   |
+------------------------+----------------------------------------------------+
| use_existing_users     | In case of testing cloud with r/o Keystone e.g. AD |
+------------------------+----------------------------------------------------+
| image_name             | Images name that exist in cloud                    |
+------------------------+----------------------------------------------------+
| flavor_name            | Flavor name that exist in cloud                    |
+------------------------+----------------------------------------------------+
| to_flavor_name         | Flavor bigger than flavor_name exist in cloud      |
+------------------------+----------------------------------------------------+
| glance_image_location  | Path of image that is used to test Glance          |
+------------------------+----------------------------------------------------+
| users_amount           | Expected amount of users                           |
+------------------------+----------------------------------------------------+
| tenants_amount         | Expected amount of tenants                         |
+------------------------+----------------------------------------------------+
| controllers_amount     | Amount of OpenStack API nodes (controllers)        |
+------------------------+----------------------------------------------------+
| external_network_id    | External network id for test                       |
+------------------------+----------------------------------------------------+
| external_network_name  | External network name for test                     |
+------------------------+----------------------------------------------------+
| private_network_id     | Private network id for test                        |
+------------------------+----------------------------------------------------+
| zone_id                | A exist DNSaaS zone id                             |
+------------------------+----------------------------------------------------+
