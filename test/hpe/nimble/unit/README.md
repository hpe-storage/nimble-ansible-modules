
Unit tests for Ansible modules for nimble array

================


## Steps to run the test.

1. Please install python 3.6 and above. ex : "pip3 install python3"

2. Download and install Nimble python SDK using pip command. ex : "pip install nimble-python-sdk" Or from the link [nimble-python-sdk](https://github.com/hpe-storage/nimble-python-sdk)

3. Edit the "storage_system_properties.yml" file present under unit\properties folder. Provide the nimble array credentials.

4. Install ansible. command : sudo yum install ansible

5. Go to /etc/ansible and run the command git clone https://github.com/hpe-storage/nimble-ansible-modules.git

6. Go to folder '/etc/ansible/nimble-ansible-modules/ansible_collection/hpe/nimble' and Run the command 'ansible-galaxy collection build --force'. This will
   create a zip file in the current folder with name 'hpe-nimble-1.0.0.tar.gz'

7. Install this ansible collection using command : 'ansible-galaxy collection install hpe-nimble-1.0.0.tar.gz --force'

8. Now go to /etc/ansible folder on command prompt as root and run the cmd : ' ansible-playbook /etc/ansible/nimble-ansible-modules/test/hpe/nimble/unit/unit_test.yml -i hosts -v '

============================
## Logging:

To collect the logs, run the below command and redirect the logs
ansible-playbook unit_test.yml  -v > ansible_unit.log

