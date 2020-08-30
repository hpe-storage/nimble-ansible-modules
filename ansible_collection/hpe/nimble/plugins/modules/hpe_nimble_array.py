#!/usr/bin/python

# Copyright 2020 Hewlett Packard Enterprise Development LP
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

# author Alok Ranjan (alok.ranjan2@hpe.com)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
author:
  - HPE Nimble Storage Ansible Team (@ar-india) <nimble-dcs-storage-automation-eng@hpe.com>
description: Manage array on HPE Nimble Storage group.
module: hpe_nimble_array
options:
  allow_lower_limits:
    required: False
    type: bool
    default : False
    description:
    - A True setting will allow you to add an array with lower limits to a pool with higher limits.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing array.
  create_pool:
    required: False
    type: bool
    default: False
    description:
    - Whether to create associated pool during array create.
  ctrlr_a_support_ip:
    required: False
    type: str
    description:
    - Controller A Support IP Address. Four numbers in the range (0,255) separated by periods.
  ctrlr_b_support_ip:
    required: False
    type: str
    description:
    - Controller B Support IP Address. Four numbers in the range (0,255) separated by periods.
  failover:
    required: False
    type: bool
    description:
    - Perform a failover on the specified array.
  force:
    required: False
    type: bool
    description:
    - Forcibly delete the specified array.
  halt:
    required: False
    type: bool
    description:
    - Halt the specified array. Restarting the array will require physically powering it back on.
  name:
    required: True
    type: str
    description:
    - The user provided name of the array. It is also the array's hostname.
  nic_list:
    required: False
    type: list
    elements: dict
    description:
    - List NICs information. Used when creating an array.
  pool_description:
    required: False
    type: str
    description:
    - Text description of the pool to be created during array creation.
  pool_name:
    required: False
    type: str
    description:
    - Name of pool to which this is a member.
  reboot:
    required: False
    type: bool
    description:
    - Reboot the specified array.
  secondary_mgmt_ip:
    required: False
    type: str
    description:
    - Secondary management IP address for the group.
  serial:
    required: False
    type: str
    description:
    - Serial number of the array.
  state:
      required: True
      choices:
          - create
          - present
          - absent
      type: str
      description:
      - Choice for array operation
extends_documentation_fragment: hpe.nimble.hpe_nimble
short_description: Manage HPE Nimble Storage array.
version_added: "2.9.0"
'''

EXAMPLES = r'''

# if state is create , then create a array if not present. Fails if already present.
# if state is present, then create a array if not present. Succeed if it already exists.
- name: Create array if not present
  hpe_nimble_array:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: "{{ state | default('present') }}"
    name: "{{ name }}"
    ctrlr_b_support_ip: "{{ ctrlr_b_support_ip | mandatory}}"
    ctrlr_a_support_ip: "{{ ctrlr_a_support_ip | mandatory}}"
    serial: "{{ serial | mandatory}}"
    nic_list: "{{ nic_list | mandatory}}"
    pool_name: "{{ pool_name | mandatory}}"

- name: Delete array
  hpe_nimble_array:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    vol_name: "{{ansible_default_ipv4['address']}}-{{ vol_name }}"
    name: "{{ name }}"
    state: absent

- name: Failover array
  hpe_nimble_array:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    failover: true
    state: present

- name: halt array
  hpe_nimble_array:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    halt: true

- name: Reboot array
  hpe_nimble_array:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    reboot: true

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils


def create_array(
        client_obj,
        array_name,
        **kwargs):

    if utils.is_null_or_empty(array_name):
        return (False, False, "Create array failed as array name is not present.", {})

    try:
        array_resp = client_obj.arrays.get(id=None, name=array_name)
        if utils.is_null_or_empty(array_resp):
            params = utils.remove_null_args(**kwargs)
            array_resp = client_obj.arrays.create(name=array_name, **params)
            if array_resp is not None:
                return (True, True, f"Created array '{array_name}' successfully.", {})
        else:
            return (False, False, f"Array '{array_name}' cannot be created as it is already present", {})
    except Exception as ex:
        return (False, False, f"Array creation failed |{ex}", {})


def update_array(
        client_obj,
        array_resp,
        **kwargs):

    if utils.is_null_or_empty(array_resp):
        return (False, False, "Update array failed as array name is not present.", {})

    try:
        array_name = array_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(array_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            array_resp = client_obj.arrays.update(id=array_resp.attrs.get("id"), **params)
            return (True, True, f"Array '{array_name}' already present. Modified the following fields:", changed_attrs_dict)
        else:
            return (True, False, f"Array '{array_name}' already present.", {})

    except Exception as ex:
        return (False, False, f"Array update failed |{ex}", {})


def delete_array(
        client_obj,
        array_name):

    if utils.is_null_or_empty(array_name):
        return (False, False, "Delete array failed as array name is not present.", {})

    try:
        array_resp = client_obj.arrays.get(id=None, name=array_name)
        if utils.is_null_or_empty(array_resp):
            return (False, False, f"Array '{array_name}' cannot be deleted as it is not present.", {})
        else:
            array_resp = client_obj.arrays.delete(id=array_resp.attrs.get("id"))
            return (True, True, f"Deleted array '{array_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Array deletion failed |{ex}", {})


def failover_array(
        client_obj,
        array_name,
        force=False):

    if utils.is_null_or_empty(array_name):
        return (False, False, "Failover array failed as array name is not present.", {})
    try:
        array_resp = client_obj.arrays.get(id=None, name=array_name)
        if utils.is_null_or_empty(array_resp):
            return (False, False, f"Array '{array_name}' cannot failover as it is not present.", {})
        else:
            array_resp = client_obj.arrays.failover(id=array_resp.attrs.get("id"), force=force)
            return (True, True, f"Failover array '{array_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Array failover failed |{ex}", {})


def halt_array(
        client_obj,
        array_name):

    if utils.is_null_or_empty(array_name):
        return (False, False, "Halt array failed as array name is not present.", {})

    try:
        array_resp = client_obj.arrays.get(id=None, name=array_name)
        if utils.is_null_or_empty(array_resp):
            return (False, False, f"Array '{array_name}' cannot be halted as it is not present.", {})
        else:
            array_resp = client_obj.arrays.halt(id=array_resp.attrs.get("id"))
            return (True, True, f"Halted array '{array_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Array Halt failed |{ex}", {})


def reboot_array(
        client_obj,
        array_name):

    if utils.is_null_or_empty(array_name):
        return (False, False, "Reboot array failed as array name is not present.", {})

    try:
        array_resp = client_obj.arrays.get(id=None, name=array_name)
        if utils.is_null_or_empty(array_resp):
            return (False, False, f"Array '{array_name}' cannot be rebooted as it is not present.", {})
        else:
            array_resp = client_obj.arrays.reboot(id=array_resp.attrs.get("id"))
            return (True, True, f"Rebooted array '{array_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Array reboot failed |{ex}", {})


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['create', 'present', 'absent'],
            "type": "str"
        },
        "name": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "pool_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "serial": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "change_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "create_pool": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "pool_description": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "allow_lower_limits": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "ctrlr_a_support_ip": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "ctrlr_b_support_ip": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "nic_list": {
            "required": False,
            "type": 'list',
            "elements": 'dict',
            "no_log": False
        },
        "secondary_mgmt_ip": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "force": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "failover": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "halt": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "reboot": {
            "required": False,
            "type": "bool",
            "no_log": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    module = AnsibleModule(argument_spec=fields)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    array_name = module.params["name"]
    change_name = module.params["change_name"]
    pool_name = module.params["pool_name"]
    serial = module.params["serial"]
    create_pool = module.params["create_pool"]
    pool_description = module.params["pool_description"]
    allow_lower_limits = module.params["allow_lower_limits"]
    ctrlr_a_support_ip = module.params["ctrlr_a_support_ip"]
    ctrlr_b_support_ip = module.params["ctrlr_b_support_ip"]
    nic_list = module.params["nic_list"]
    secondary_mgmt_ip = module.params["secondary_mgmt_ip"]
    force = module.params["force"]
    failover = module.params["failover"]
    halt = module.params["halt"]
    reboot = module.params["reboot"]

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
    if state == "present" and failover is True:
        return_status, changed, msg, changed_attrs_dict = failover_array(client_obj, array_name, force)

    elif state == "present" and halt is True:
        return_status, changed, msg, changed_attrs_dict = halt_array(client_obj, array_name)

    elif state == "present" and reboot is True:
        return_status, changed, msg, changed_attrs_dict = reboot_array(client_obj, array_name)

    elif ((failover is None or failover is False)
          and (halt is None or halt is False)
          and (reboot is None or reboot is False)
          and (state == "create" or state == "present")):

        array_resp = client_obj.arrays.get(name=array_name)
        if array_resp is None or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_array(
                client_obj,
                array_name,
                pool_name=pool_name,
                serial=serial,
                create_pool=create_pool,
                pool_description=pool_description,
                allow_lower_limits=allow_lower_limits,
                ctrlr_a_support_ip=ctrlr_a_support_ip,
                ctrlr_b_support_ip=ctrlr_b_support_ip,
                nic_list=nic_list,
                secondary_mgmt_ip=secondary_mgmt_ip,
                force=force,
                failover=failover,
                halt=halt,
                reboot=reboot)
        else:
            return_status, changed, msg, changed_attrs_dict = update_array(
                client_obj,
                array_resp,
                name=change_name,
                force=force)
    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_array(client_obj, array_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
