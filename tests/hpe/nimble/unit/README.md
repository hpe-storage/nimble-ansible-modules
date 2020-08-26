
Unit tests for Ansible modules for nimble array

================


## PREREQUISITE.

1. Please install python 3.6 and above. ex : "pip install python3"

2. Download and install Nimble python SDK using pip command. ex : "pip install nimble-python-sdk" Or from the link [nimble-python-sdk](https://github.com/hpe-storage/nimble-python-sdk)

3. Edit the "storage_system_properties.yml" file present under unit\properties folder. Provide the nimble array credentials.

4. Install Ansible 2.9 and above. How to install Link [Ansible installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

============================

## Execution

1. Open a putty session and go to the folder "tests/hpe/nimble/unit".
2. Run the command "ansible-playbook unit_test.yml  -v > ansible_unit.log"

## Logging:

To collect the logs, run the below command and redirect the logs
ansible-playbook unit_test.yml  -v > ansible_unit.log

