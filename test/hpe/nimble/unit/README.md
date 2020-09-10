
Unit tests for Ansible modules for nimble array

================


## PREREQUISITE.

1. Please install python 3.6 and above. ex : "pip install python3"

2. Download and install Nimble python SDK using pip command. ex : "pip install nimble-python-sdk" Or from the link [nimble-python-sdk](https://github.com/hpe-storage/nimble-python-sdk)

3. Edit the "storage_system_properties.yml" file present under unit\properties folder. Provide the nimble array credentials.

============================
## Logging:

To collect the logs, run the below command and redirect the logs
ansible-playbook unit_test.yml  -v > ansible_unit.log

