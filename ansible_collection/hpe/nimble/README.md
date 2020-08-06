
# HPE Nimble Storage Ansible Collection



## Prerequisites



- Ansible 2.10 or later

- HPE Nimble Storage array running NimbleOS 5.0 or later

- HPE Nimble Storage SDK for Python

- Python >=v3.6




## Installation




Install the HPE Nimble Storage array collection on your Ansible management host.




- Install the collection using the following command:
`ansible-galaxy collection install git+https://github.com/hpe-storage/nimble-ansible-modules.git,rel-1.0.0`


- Above command will install the collection in /root/.ansible/collections/ansible_collections



- To install in a custom folder, please use the following command:

	 `ansible-galaxy collection install git+https://github.com/hpe-storage/nimble-ansible-modules.git,rel-1.0.0 -p /usr/share/ansible/collections` .
 This will install the collection under usr/share/ansible/collections.




**Note**: This is a beta release. The above steps will finally be removed once we upload and publish our collection on galaxy server and will be replaced with the official way to install a ansible collection.



## Available Modules



- hpe_nimble_access_control_record - Manage HPE Nimble Storage access control records
- hpe_nimble_info - Collect information from HPE Nimble Storage array
- hpe_nimble_initiator_group - Manage HPE Nimble Storage initiator groups
- hpe_nimble_volume - Manage HPE Nimble Storage volumes


## License



[Apache-2.0-or-later](http://www.apache.org/licenses/LICENSE-2.0)