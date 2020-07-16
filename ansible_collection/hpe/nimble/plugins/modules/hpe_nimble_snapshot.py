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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
author:
  - Alok Ranjan (@ar-india)
description: Manage snapshots on HPE Nimble Storage group.
module: hpe_nimble_snapshot
options:
  agent_type:
    required: False
    choices:
    - none
    - smis
    - vvol
    - openstack
    - openstackv2
    type: str
    default: none
    description:
    - External management agent type.
  app_uuid:
    required: False
    type: str
    description:
    - Application identifier of snapshot.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing snapshot.
  description:
    required: False
    type: str
    description:
    - Text description of snapshot.
  expiry_after:
    required: False
    type: int
    description:
    - Number of seconds after which this snapshot is considered expired by snapshot TTL. A value of 0 indicates that snapshot never expires.
  force:
    required: False
    type: bool
    default: False
    description:
    - Forcibly delete the specified snapshot even if it is the last replicated collection. Doing so could lead to full re-seeding at the next replication.
  metadata:
    required: False
    type: dict
    description:
    - Key-value pairs that augment a snapshot's attributes. List of key-value pairs. Keys must be unique and non-empty.
  name:
    required: True
    type: str
    description:
    - Name of snapshot.
  online:
    required: False
    type: bool
    default: False
    description:
    - Online state for a snapshot means it could be mounted for data restore.
  state:
    required: True
    choices:
    - present
    - absent
    - create
    type: str
    description:
    - Choice for snapshot state.
  volume:
    required: True
    type: str
    description:
    - Parent volume name.
  writable:
    required: False
    type: bool
    default: False
    description:
    - Allow snapshot to be writable. Mandatory and must be set to 'true' for VSS application synchronized snapshots.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage snapshots.
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create , then create a snapshot if not present. Fails if already present.
# if state is present, then create a snapshot if not present. Succeeds if it already exists.
- name: Create snapshot if not present
  hpe_nimble_snapshot:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: "{{ state | default('present') }}"
    volume: "{{ volume }}"
    name: "{{ name }}"
    online: "{{ online | default(true) }}"
    writable: "{{ writable | default(false) }}"

- name: Delete snapshot  (must be offline)
  hpe_nimble_snapshot:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    volume: "{{ volume }}"
    name: "{{ name }}"
    state: absent

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils


def create_snapshot(
        client_obj,
        vol_name,
        snapshot_name,
        **kwargs):

    if utils.is_null_or_empty(snapshot_name):
        return (False, False, "Create snapshot failed as snapshot is not present.", {})
    if utils.is_null_or_empty(vol_name):
        return (False, False, "Create snapshot failed as volume is not present.", {})

    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if utils.is_null_or_empty(vol_resp):
            return (False, False, f"Volume '{vol_name}' not present on array for taking snapshot.", {})
        snap_resp = client_obj.snapshots.get(id=None, vol_name=vol_name, name=snapshot_name)
        if utils.is_null_or_empty(snap_resp):
            params = utils.remove_null_args(**kwargs)
            snap_resp = client_obj.snapshots.create(name=snapshot_name,
                                                    vol_id=vol_resp.attrs.get("id"),
                                                    **params)
            if snap_resp is not None:
                return (True, True, f"Snapshot '{snapshot_name}' created successfully.", {})
        else:
            return (False, False, f"Snapshot '{snapshot_name}' cannot be created as it is already present.", {})
    except Exception as ex:
        return (False, False, f"Snapshot creation failed | {ex}", {})


def update_snapshot(
        client_obj,
        snap_resp,
        **kwargs):

    if utils.is_null_or_empty(snap_resp):
        return (False, False, "Update snapshot failed as snapshot is not present.", {})

    try:
        snapshot_name = snap_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(snap_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            snap_resp = client_obj.snapshots.update(id=snap_resp.attrs.get("id"), **params)
            return (True, True, f"Snapshot '{snapshot_name}' already present. Modified the following fields:", changed_attrs_dict)
        else:
            return (True, False, f"Snapshot '{snapshot_name}' already present.", {})

    except Exception as ex:
        return (False, False, f"Snapshot update failed | {ex}", {})


def delete_snapshot(
        client_obj,
        vol_name,
        snapshot_name):

    if utils.is_null_or_empty(snapshot_name):
        return (False, False, "Delete snapshot failed as snapshot is not present.", {})
    if utils.is_null_or_empty(vol_name):
        return (False, False, "Delete snapshot failed. Volume is not present.", {})

    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if utils.is_null_or_empty(vol_resp):
            return (False, False, f"Volume '{vol_name}' is not present on Array for deleting snapshot.", {})
        snap_resp = client_obj.snapshots.get(id=None, vol_name=vol_name, name=snapshot_name)
        if utils.is_null_or_empty(snap_resp):
            return (False, False, f"Snapshot '{snapshot_name}' cannot be deleted as it is not present in given volume '{vol_name}'.", {})
        else:
            client_obj.snapshots.delete(id=snap_resp.attrs.get("id"))
            return (True, True, f"Deleted snapshot '{snapshot_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Snapshot deletion failed | {ex}", {})


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present',
                        'absent',
                        'create'
                        ],
            "type": "str"
        },
        "change_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "name": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "description": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "volume": {
            "required": True,
            "type": "str"
        },
        "online": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "writable": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "app_uuid": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "metadata": {
            "required": False,
            "type": "dict"
        },
        "agent_type": {
            "required": False,
            "choices": ['none', 'smis', 'vvol', 'openstack', 'openstackv2'],
            "type": "str"
        },
        "expiry_after": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "force": {
            "required": False,
            "type": "bool",
            "default": False,
            "no_log": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    required_if = [('state', 'create', ['volume'])]

    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    snapshot_name = module.params["name"]
    change_name = module.params["change_name"]
    description = module.params["description"]
    vol_name = module.params["volume"]
    online = module.params["online"]
    writable = module.params["writable"]
    app_uuid = module.params["app_uuid"]
    metadata = module.params["metadata"]
    agent_type = module.params["agent_type"]
    expiry_after = module.params["expiry_after"]
    force = module.params["force"]

    if (username is None or password is None or hostname is None or snapshot_name is None):
        module.fail_json(
            msg="Storage system IP or username or password is null or snapshot name is null.")

    client_obj = client.NimOSClient(
        hostname,
        username,
        password
    )
    # defaults
    return_status = changed = False
    msg = "No task to run."

    # States
    if state == "create" or state == "present":
        snap_resp = client_obj.snapshots.get(id=None, vol_name=vol_name, name=snapshot_name)
        if utils.is_null_or_empty(snap_resp) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_snapshot(
                client_obj,
                vol_name,
                snapshot_name,
                description=description,
                online=online,
                writable=writable,
                app_uuid=app_uuid,
                metadata=metadata,
                agent_type=agent_type)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_snapshot(
                client_obj,
                snap_resp,
                name=change_name,
                description=description,
                online=online,
                expiry_after=expiry_after,
                app_uuid=app_uuid,
                metadata=metadata,
                force=force)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_snapshot(
            client_obj,
            vol_name,
            snapshot_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
