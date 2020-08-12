# HPE Nimble Storage Content Collection for Ansible

This is a pre-release of the HPE Nimble Storage Content Collection for Ansible.

## Requirements

- Ansible 2.10 or later
- HPE Nimble Storage arrays running NimbleOS 5.0 or later
- HPE Nimble Storage SDK for Python
- Python >=v3.6

## Installation

Install the collection on your Ansible management host.

```
ansible-galaxy collection install git+https://github.com/hpe-storage/nimble-ansible-modules.git#ansible_collection/hpe/nimble,rel-1.0.0
```

**Note**: This is a beta release. The content collection will be made available through Ansible Galaxy and Automation Hub upon release.

## Documentation

A [local rendering](https://hpe-storage.github.io/nimble-ansible-modules/modules/list_of_storage_modules.html) of the Ansible documentation for the available modules:

- [hpe_nimble_volume](https://hpe-storage.github.io/nimble-ansible-modules/modules/hpe_nimble_volume_module.html#hpe-nimble-volume-module)
- [hpe_nimble_initiator_group](https://hpe-storage.github.io/nimble-ansible-modules/modules/hpe_nimble_initiator_group_module.html#hpe-nimble-initiator-group-module)
- [hpe_nimble_access_control_record](https://hpe-storage.github.io/nimble-ansible-modules/modules/hpe_nimble_access_control_record_module.html#hpe-nimble-access-control-record-module)
- [hpe_nimble_info](https://hpe-storage.github.io/nimble-ansible-modules/modules/hpe_nimble_info_module.html#hpe-nimble-info-module)

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
