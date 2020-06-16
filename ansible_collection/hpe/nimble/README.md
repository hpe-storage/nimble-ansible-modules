# HPE Nimble Storage Ansible Collection

=============================================================
Copyright (c) 2020 HPE Nimble, Inc. All rights reserved.
Specifications subject to change without notice.
=============================================================


## Prerequisites

- Ansible 2.9 or later
- HPE Nimble Storage Array running NimOs 5.1 or later
- nimble python SDK 1.0.0 or higher
- Python >=v3.6

# Installation

Install the HPE Nimble Storage Array collection on your Ansible management host.

```bash
ansible-galaxy collection install hpe.nimble
```
To use Collection add the following to the top of your playbook
```
collections:
  - hpe.nimble
```

# Need help
To BE DONE later

## Available Modules

- hpe_nimble_volume -  Manage volume on a Nimble Storage group
- hpe_nimble_acr - Manages a HPE Nimble Storage Access Control Record

## License

[Apache-2.0-or-later](http://www.apache.org/licenses/LICENSE-2.0)

## Author

This collection was created in 2020 by [Alok Ranjan](@ranjanal) for, and on behalf of, the [HPE Nimble Storage Ansible Team](hpenimble-ansible-team@hpe.com)

# Release Notes

## 1.0.0
