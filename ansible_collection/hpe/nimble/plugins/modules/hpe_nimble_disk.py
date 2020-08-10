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
description: Manage disks on HPE Nimble Storage group.
module: hpe_nimble_disk
options:
  disk_op:
    required: True
    choices:
    - add
    - remove
    type: str
    description:
    - The intended operation to be performed on the specified disk.
  force:
    required: False
    type: bool
    default: False
    description:
    - Forcibly add a disk.
  shelf_location:
    required: True
    type: str
    description:
    - Position of the shelf the disk belongs to.
  slot:
    required: True
    type: str
    description:
    - Disk slot number.
  state:
    required: True
    choices:
    - present
    type: str
    description:
    - Choice for disk operation.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage disk.
version_added: 2.9
'''

EXAMPLES = r'''

- name: Update Disk
  hpe_nimble_disk:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    slot: "{{ slot | mandatory }}"
    shelf_location: "{{ shelf_location | mandatory }}"
    disk_op: "{{ disk_op | mandatory }}"
    force: "{{ force }}"
    state: present

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils

def update_disk(
        client_obj,
        slot,
        shelf_location,
        disk_op,
        force=False):

    if utils.is_null_or_empty(shelf_location):
        return (False, False, "Disk update failed as no shelf location provided.", {})

    try:
        # get the details of the disk for a given slot and shelf_location
        disk_resp = client_obj.disks.list(detail=True)
        if disk_resp is None:
            return (False, False, "No Disk is present on array.", {})
        else:
            disk_id = None
            changed_attrs_dict = {}
            for disk_obj in disk_resp:
                if slot == disk_obj.attrs.get("slot") and shelf_location == disk_obj.attrs.get("shelf_location"):
                    disk_id = disk_obj.attrs.get("id")
                    break
            disk_resp = client_obj.disks.update(id=disk_id, disk_op=disk_op, force=force)
            changed_attrs_dict['slot'] = slot
            changed_attrs_dict['shelf_location'] = shelf_location
            return (True, True, f"Successfully updated disk to slot '{slot}' at shelf location '{shelf_location}'.", changed_attrs_dict)
    except Exception as ex:
        return (False, False, f"Disk update failed |'{ex}'", {})


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present'],
            "type": "str"
        },
        "disk_op": {
            "required": True,
            "choices": ['add', 'remove'],
            "type": "str",
            "no_log": False
        },
        "slot": {
            "required": True,
            "type": "int",
            "no_log": False
        },
        "shelf_location": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "force": {
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
    disk_op = module.params["disk_op"]
    slot = module.params["slot"]
    shelf_location = module.params["shelf_location"]
    force = module.params["force"]

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
    if state == "present":
        return_status, changed, msg, changed_attrs_dict = update_disk(
            client_obj,
            slot,
            shelf_location,
            disk_op,
            force)

    if return_status:
        if not utils.is_null_or_empty(changed_attrs_dict) and changed_attrs_dict.__len__() > 0:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, message=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
