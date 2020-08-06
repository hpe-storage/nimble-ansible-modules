
# HPE Nimble Storage Ansible Collections

There are currently 1 HPE Nimble Storage Collections

<Link  to  be  published  at  the  time  of  release>


## Requirements

- Ansible 2.10 or later

- HPE Nimble Storage array running NimbleOS 5.0 or later

- HPE Nimble Storage SDK for Python

- Python >=v3.6


## Installation


Install the HPE Nimble Storage array collection on your Ansible management host.


- Install the collection using the following command `ansible-galaxy collection install git+https://github.com/hpe-storage/nimble-ansible-modules.git,rel-1.0.0`

- Above command will install the collection in /root/.ansible/collections/ansible_collections

- To install in a custom folder, please use the following command, `ansible-galaxy collection install git+https://github.com/hpe-storage/nimble-ansible-modules.git,rel-1.0.0 -p /usr/share/ansible/collections` . This will install the collection under usr/share/ansible/collections.



**Note**: This is a beta release. The above steps will finally be removed once we upload and publish our collection on galaxy server and will be replaced with the official way to install a ansible collection.

## License

[Apache-2.0-or-later](http://www.apache.org/licenses/LICENSE-2.0)