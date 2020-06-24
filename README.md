# HPE Nimble Storage Ansible Collections

There are currently 1 HPE Nimble Storage Collections
<Link to be published at the time of release>
## Requirements
- ansible version >= 2.9

## Installation

Install the HPE Nimble Storage array collection on your Ansible management host.

- Download the collection from here [Nimble-Ansible-collection-builds](https://confluence.eng.nimblestorage.com/display/IFP/Ansible+Storage+Modules#AnsibleStorageModules-AnsibleCollectionBuilds:)
- Go to the downloaded path and run cmd " ansible-galaxy collection install <package-name.tar.gz>". Ex: ansible-galaxy collection install hpe-nimble-1.0.0.tar.gz.
- Above command will install the collection in /root/.ansible/collections/ansible_collections

**Note**: The above steps will finally be removed once we upload and publish our collection on galaxy server and will be replaced with the official way to install a ansible collection.

## License

[Apache-2.0-or-later](http://www.apache.org/licenses/LICENSE-2.0)
