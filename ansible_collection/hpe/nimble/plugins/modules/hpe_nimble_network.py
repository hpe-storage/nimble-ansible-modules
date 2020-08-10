#!/usr/bin/python

# # Copyright 2020 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# author alok ranjan (alok.ranjan2@hpe.com)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
author:
  - Alok Ranjan (@ar-india)
description: Manage storage network config on HPE Nimble Storage group.
module: hpe_nimble_network
options:
  activate:
    required: False
    type: bool
    description:
    - Activate a network configuration.
  array_list:
    required: False
    type: list
    description:
    - List of array network configs.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing network config.
  iscsi_automatic_connection_method:
    required: False
    type: bool
    description:
    - Whether automatic connection method is enabled. Enabling this means means redirecting connections from the specified iSCSI
      discovery IP address to the best data IP address based on connection counts.
  iscsi_connection_rebalancing:
    required: False
    type: bool
    default: True
    description:
    - Whether rebalancing is enabled. Enabling this means rebalancing iSCSI connections by periodically breaking existing
      connections that are out-of-balance, allowing the host to reconnect to a more appropriate data IP address.
  ignore_validation_mask:
    required: False
    type: int
    description:
    - Indicates whether to ignore the validation.
  mgmt_ip:
    required: False
    type: str
    description:
    - Management IP address for the Group. Four numbers in the range (0,255) separated by periods.
  name:
    required: True
    type: str
    choices:
    -  active
    -  backup
    -  draft
    description:
    - Name of the network configuration. Use the name 'draft' when creating a draft configuration.
  secondary_mgmt_ip:
    required: False
    type: str
    description:
    - Secondary management IP address for the Group. Four numbers in the range [0,255] separated by periods.
  subnet_list:
    required: False
    type: list
    description:
    - List of subnet configs.
  route_list:
    required: False
    type: list
    description:
    - List of static routes.
  state:
    required: True
    choices:
    -  create
    -  present
    -  absent
    type: str
    description:
    - Choice for network config operation.
  validate:
    required: False
    type: bool
    description:
    - Validate a network configuration.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage network configuration.
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create, then create network config, fails if it exist or cannot create
# if state is present, then create network config if not present ,else success
- name: Create network config
  hpe_nimble_network:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    route: "{{ route }}"
    subnet: "{{ subnet }}"
    array: "{{ array }}"
    iscsi_automatic_connection_method: true
    iscsi_connection_rebalancing: False
    mgmt_ip: "{{ mgmt_ip }}"
    state: "{{ state | default('present') }}"

- name: Delete network config
  hpe_nimble_network:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: "absent"

- name: Validate network config
  hpe_nimble_network:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: "present"
    ignore_validation_mask: 1
    validate: true

- name: Activate Network config
  hpe_nimble_network:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: "present"
    ignore_validation_mask: 1
    activate: true

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils


def create_update_network_config(
        client_obj,
        name,
        state,
        iscsi_automatic_connection_method,
        iscsi_connection_rebalancing,
        mgmt_ip,
        change_name,
        **kwargs):

    if utils.is_null_or_empty(name):
        return (False, False, "Create network config failed as name is not present.", {})

    try:
        network_resp = client_obj.network_configs.get(id=None, name=name)
        if utils.is_null_or_empty(network_resp):
            params = utils.remove_null_args(**kwargs)
            network_resp = client_obj.network_configs.create(name=name,
                                                             iscsi_automatic_connection_method=iscsi_automatic_connection_method,
                                                             iscsi_connection_rebalancing=iscsi_connection_rebalancing,
                                                             mgmt_ip=mgmt_ip,
                                                             **params)
            return (True, True, f"Network config '{name}' created successfully.", {})
        else:
            if state == "create":
                return (False, False, f"Network config '{name}' cannot be created as it is already present.", {})

            # update case
            kwargs['name'] = change_name
            changed_attrs_dict, params = utils.remove_unchanged_or_null_args(network_resp, **kwargs)
            if changed_attrs_dict.__len__() > 0:
                network_resp = client_obj.network_configs.update(id=network_resp.attrs.get("id"),
                                                                 iscsi_automatic_connection_method=iscsi_automatic_connection_method,
                                                                 iscsi_connection_rebalancing=iscsi_connection_rebalancing,
                                                                 mgmt_ip=mgmt_ip,
                                                                 **params)
                return (True, True, f"Network config '{name}' already present. Modified the following fields:", changed_attrs_dict)
            else:
                return (True, False, f"Network config '{network_resp.attrs.get('name')}' already present.", {})
    except Exception as ex:
        return (False, False, f"Network config creation failed |'{ex}'", {})


def delete_network_config(
        client_obj,
        name):

    if utils.is_null_or_empty(name):
        return (False, False, "Delete network config failed as name is not present.", {})

    try:
        network_resp = client_obj.network_configs.get(id=None, name=name)
        if utils.is_null_or_empty(network_resp):
            return (False, False, f"Network config '{name}' cannot be deleted as it is not present.", {})

        client_obj.network_configs.delete(id=network_resp.attrs.get("id"))
        return (True, True, f"Deleted network config '{name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Delete network config failed |'{ex}'", {})


def validate_network_config(
        client_obj,
        name,
        ignore_validation_mask):

    if utils.is_null_or_empty(name):
        return (False, False, "Validate network config failed as name is not present.", {})

    try:
        network_resp = client_obj.network_configs.get(id=None, name=name)
        if utils.is_null_or_empty(network_resp):
            return (False, False, f"Network config '{name}' cannot be validated as it is not present.", {})

        client_obj.network_configs.validate_netconfig(
            id=network_resp.attrs.get("id"),
            ignore_validation_mask=ignore_validation_mask)

        return (True, False, f"Validated network config '{name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Validate Network config failed |'{ex}'", {})


def activate_network_config(
        client_obj,
        name,
        ignore_validation_mask):

    if utils.is_null_or_empty(name):
        return (False, False, "Activate network config failed as name is not present.", {})

    try:
        network_resp = client_obj.network_configs.get(id=None, name=name)
        if utils.is_null_or_empty(network_resp):
            return (False, False, f"Network config '{name}' cannot be activated as it is not present.", {})

        client_obj.network_configs.activate_netconfig(id=network_resp.attrs.get("id"),
                                                      ignore_validation_mask=ignore_validation_mask)

        return (True, True, f"Activated network config '{name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Activate Network config failed |'{ex}'", {})


def main():

    fields = {
        "activate": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "array": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "change_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "iscsi_automatic_connection_method": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "iscsi_connection_rebalancing": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "ignore_validation_mask": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "mgmt_ip": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "name": {
            "required": True,
            "choices": ['active',
                        'backup',
                        'draft'
                        ],
            "type": "str",
            "no_log": False
        },
        "secondary_mgmt_ip": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "subnet": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "route": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "state": {
            "required": True,
            "choices": ['create',
                        'present',
                        'absent'
                        ],
            "type": "str"
        },
        "validate": {
            "required": False,
            "type": "bool",
            "no_log": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    required_if = [('state', 'create', ['array', 'iscsi_automatic_connection_method', 'iscsi_connection_rebalancing', 'mgmt_ip', 'subnet', 'route'])]
    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    activate = module.params["activate"]
    array = module.params["array"]
    iscsi_automatic_connection_method = module.params["iscsi_automatic_connection_method"]
    iscsi_connection_rebalancing = module.params["iscsi_connection_rebalancing"]
    ignore_validation_mask = module.params["ignore_validation_mask"]
    mgmt_ip = module.params["mgmt_ip"]
    name = module.params["name"]
    change_name = module.params["change_name"]
    secondary_mgmt_ip = module.params["secondary_mgmt_ip"]
    subnet = module.params["subnet"]
    route = module.params["route"]
    state = module.params["state"]
    validate = module.params["validate"]

    if (username is None or password is None or hostname is None):
        module.fail_json(
            msg="Missing variables: hostname, username and password is mandatory.")

    client_obj = client.NimOSClient(
        hostname,
        username,
        password
    )
    # defaults
    return_status = changed = False
    msg = "No task to run."

    # States
    if ((validate is None or validate is False)
        and (activate is None or activate is False)
            and (state == "create" or state == "present")):
        # if not client_obj.network_configs.get(id=None, name=name) or state == "create":
        return_status, changed, msg, changed_attrs_dict = create_update_network_config(
            client_obj,
            name,
            state,
            iscsi_automatic_connection_method,
            iscsi_connection_rebalancing,
            mgmt_ip,
            change_name,
            array_list=array,
            ignore_validation_mask=ignore_validation_mask,
            secondary_mgmt_ip=secondary_mgmt_ip,
            subnet_list=subnet,
            route_list=route)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_network_config(client_obj, name)

    elif state == "present" and validate is True:
        return_status, changed, msg, changed_attrs_dict = validate_network_config(client_obj, name, ignore_validation_mask)

    elif state == "present" and activate is True:
        return_status, changed, msg, changed_attrs_dict = activate_network_config(client_obj, name, ignore_validation_mask)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
