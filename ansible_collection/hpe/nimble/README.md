# HPE Nimble Storage Ansible Collection

## Prerequisites

- Ansible 2.9 or later
- HPE Nimble Storage array running NimbleOS 5.1 or later
- HPE Nimble Storage SDK for Python
- Python >=v3.6

# Installation

Install the HPE Nimble Storage array collection on your Ansible management host.

- Download the collection from here [\ansible-collection-builds\] https://confluence.eng.nimblestorage.com/display/IFP/Ansible+Storage+Modules#AnsibleStorageModules-AnsibleCollectionBuilds:
- Go to the downloaded path and run cmd " ansible-galaxy collection install <package-name.tar.gz>". Ex: ansible-galaxy collection install hpe-nimble-1.0.0.tar.gz.
- Above command will install the collection in /root/.ansible/collections/ansible_collections

**Note**: The above steps will finally be removed once we upload and publish our collection on galaxy server and will be replaced with the official way to install a ansible collection.

## Available Modules

- hpe_nimble_acr - Manages a HPE Nimble Storage access control record
- hpe_nimble_initiator_group - Manage HPE Nimble Storage initiator group
- hpe_nimble_volume -  Manage volume on a Nimble Storage group
- hpe_nimble_volume_collection - Manage HPE Nimble Storage volume collection

## License

[Apache-2.0-or-later](http://www.apache.org/licenses/LICENSE-2.0)
