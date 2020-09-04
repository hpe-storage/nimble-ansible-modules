# HPE Nimble Storage Content Collection for Ansible

## Requirements

- Ansible 2.9 or later
- HPE Nimble Storage arrays running NimbleOS 5.0 or later
- HPE Nimble Storage SDK for Python
- Python >=v3.6

## Installation

Install the HPE Nimble Storage array collection on your Ansible management host.

- Download the collection.
- Go to the downloaded path and run cmd " ansible-galaxy collection install <package-name.tar.gz>". Ex: ansible-galaxy collection install hpe-nimble-1.0.0.tar.gz.
- Above command will install the collection in /root/.ansible/collections/ansible_collections

**Note**: The above steps will finally be removed once we upload and publish our collection on galaxy server and will be replaced with the official way to install a ansible collection.

## Available Modules

- hpe_nimble_access_control_record - Manage HPE Nimble Storage access control records
- hpe_nimble_array - Manage HPE Nimble Storage array
- hpe_nimble_chap_user - Manage HPE Nimble Storage CHAP users
- hpe_nimble_disk - Manage HPE Nimble Storage disks
- hpe_nimble_encryption - Manage HPE Nimble Storage encryption
- hpe_nimble_fc - Manage HPE Nimble Storage fibre channel
- hpe_nimble_group -  Manage HPE Nimble Storage groups
- hpe_nimble_info - Collect information from HPE Nimble Storage array
- hpe_nimble_initiator_group - Manage HPE Nimble Storage initiator groups
- hpe_nimble_network - Manage HPE Nimble Storage network configuration
- hpe_nimble_partner - Manage HPE Nimble Storage replication partners
- hpe_nimble_performance_policy - Manage HPE Nimble Storage performance policies
- hpe_nimble_pool - Manage HPE Nimble Storage pools
- hpe_nimble_protection_schedule - Manage HPE Nimble Storage protection schedules
- hpe_nimble_protection_template - Manage HPE Nimble Storage protection templates
- hpe_nimble_shelf - Manage HPE Nimble Storage shelves
- hpe_nimble_snapshot_collection - Manage HPE Nimble Storage snapshot collections
- hpe_nimble_snapshot - Manage HPE Nimble Storage snapshots
- hpe_nimble_user -  Manage HPE Nimble Storage users
- hpe_nimble_user_policy -  Manage HPE Nimble Storage user policies
- hpe_nimble_volume -  Manage HPE Nimble Storage volumes
- hpe_nimble_volume_collection - Manage HPE Nimble Storage volume collections

## License

HPE Nimble Storage Content Collection for Ansible is released under the Apache-2.0 license.

    Copyright 2020 Hewlett Packard Enterprise Development LP
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
See [LICENSE](https://github.com/hpe-storage/nimble-ansible-modules/blob/master/LICENSE) for the full terms.
