
Unit tests for Ansible modules for nimble array

================


## Steps to run the test on centos. You can use any unix flavours. Please run the steps as root user

1. Please install python 3.6 and above. ex : "sudo dnf install python3"

2. Download and install Nimble python SDK using pip command. ex : "pip3 install nimble-sdk" Or from the link [nimble-python-sdk](https://github.com/hpe-storage/nimble-python-sdk)

3. Edit the "storage_system_properties.yml" file present under unit\properties folder. Populate the varibales with correct values.

4. Install ansible using command : 'pip3 install ansible --user'

5. Make sure sshd service is running. 'sudo systemctl status sshd'

6. Go to /etc/ansible folder and run the command: 'git clone https://github.com/hpe-storage/nimble-ansible-modules.git'

7. Go to folder '/etc/ansible/nimble-ansible-modules/ansible_collection/hpe/nimble' and Run the command: 'ansible-galaxy collection build --force'.
   This will create a zip file in the current folder with name 'hpe-nimble-1.0.0.tar.gz'

8. Install this ansible collection using command : 'ansible-galaxy collection install hpe-nimble-1.0.0.tar.gz --force'

9. Now go to /etc/ansible folder on command prompt and run the cmd : ' ansible-playbook /etc/ansible/nimble-ansible-modules/test/hpe/nimble/unit/unit_test.yml -i hosts -v '

============================
## Logging:

To collect the logs, run the below command and redirect the logs
ansible-playbook unit_test.yml  -v > ansible_unit.log

