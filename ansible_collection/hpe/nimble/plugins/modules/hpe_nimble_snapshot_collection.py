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
  - Alok Ranjan (@ranjanal)
description: description: Manage snapshot collections on HPE Nimble Storage group.
module: hpe_nimble_snapshot_collection
options:
  agent_type:
    required: False
    type: str
    description:
    - External management agent type for snapshots being created as part of snapshot collection.
  allow_writes:
    required: False
    type: bool
    default: False
    description:
    - Allow applications to write to created snapshot(s). Mandatory and must be set to 'true' for VSS application synchronized snapshots.
  description:
    required: False
    type: str
    description:
    - Text description of snapshot collection.
  disable_appsync:
    required: False
    type: bool
    default: False
    description:
    - Do not perform application synchronization for this snapshot. Create a crash-consistent snapshot instead.
  expiry_after:
    required: False
    type: int
    description:
    - Number of seconds after which this snapcoll is considered expired by the snapshot TTL. A value of 0 indicates that the snapshot
      never expires, 1 indicates that the snapshot uses a group-level configured TTL value and any other value indicates the number of seconds.
  force:
    required: False
    type: bool
    default: False
    description:
    - Forcibly delete the specified snapshot collection even if it is the last replicated snapshot. Doing so could lead to full re-seeding at the next replication.
  invoke_on_upstream_partner:
    required: False
    type: bool
    default: False
    description:
    - Invoke snapshot request on upstream partner. This operation is not supported for synchronous replication volume vollections.
  is_external_trigger:
    required: False
    type: bool
    default: False
    description:
    - Is externally triggered.
  metadata:
    required: False
    type: dict
    description:
    - Key-value pairs that augment a snapshot collection attributes. List of key-value pairs. Keys must be unique and non-empty.
  name:
    required: True
    type: str
    default: None
    description:
    - Name for snapshot collection.
  replicate_to:
    required: False
    type: str
    description:
    - Specifies the partner name that the snapshots in this snapshot collection are replicated to.
  skip_db_consistency_check:
    required: False
    type: bool
    default: False
    description:
    - Skip consistency check for database files on this snapshot. This option only applies to volume collections with application synchronization set to VSS,
      application ID set to MS Exchange 2010 or later with Database Availability Group (DAG), snap_verify option set to true, and disable_appsync option set to false.
  snap_verify:
      required: False
      type: bool
      default: False
      description:
      - Run verification tool on this snapshot. This option can only be used with a volume collection that has application synchronization.
  start_online:
      required: False
      type: bool
      default: False
      description:
      - Start with snapshot set online.
  state:
      required: True
      choices:
      - present
      - absent
      - create
      type: str
      description:
      - Choice for snapshot collection operation.
  vol_snap_attr_list:
      required: False
      type: list
      description:
      - List of snapshot attributes for snapshots being created as part of snapshot collection creation. List of volumes with per snapshot attributes.
  volcoll:
      required: False
      type: str
      description:
      - Parent volume collection name.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage snapshot collections.
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create , then create a snapshot collection if not present. Fails if already present.
# if state is "present", then create a snapshot collection if not present. Succeeds if it already exists
- name: Create snapshot collection if not present
  hpe_nimble_snapshot_collection:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: "{{ state | default('present') }}"
    name: "{{ name | mandatory}}"
    volcoll: "{{ volcoll | mandatory}}"
    description: "{{ description }}"

- name: Delete snapshot collection collection  (must be offline)
  hpe_nimble_snapshot_collection:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
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


def create_snapcoll(
        client_obj,
        snapcoll_name,
        **kwargs):

    if utils.is_null_or_empty(snapcoll_name):
        return (False, False, "Create snapshot collection failed. snapshot collection name is not present.", {})
    try:
        snapcoll_resp = client_obj.snapshot_collections.get(id=None, name=snapcoll_name)
        if utils.is_null_or_empty(snapcoll_resp):
            params = utils.remove_null_args(**kwargs)
            snapcoll_resp = client_obj.snapshot_collections.create(name=snapcoll_name, **params)
            return (True, True, f"Created snapshot collection '{snapcoll_name}' successfully.", {})
        else:
            return (False, False, f"Snapshot collection '{snapcoll_name}' cannot be created as it is already present.", {})
    except Exception as ex:
        return (False, False, f"Snapshot collection creation failed | {ex}", {})


def update_snapcoll(
        client_obj,
        snapcoll_resp,
        **kwargs):

    if utils.is_null_or_empty(snapcoll_resp):
        return (False, False, "Update snapshot collection failed as snapshot collection is not present.", {})
    try:
        snapcoll_name = snapcoll_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(snapcoll_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            snapcoll_resp = client_obj.snapshot_collections.update(id=snapcoll_resp.attrs.get("id"), **params)
            return (True, True, f"Snapshot collection '{snapcoll_name}' already Present. Modified the following fields :", changed_attrs_dict)
        else:
            return (True, False, f"Snapshot collection '{snapcoll_name}' already present.", {})
    except Exception as ex:
        return (False, False, f"Snapshot collection update failed | {ex}", {})


def delete_snapcoll(client_obj, snapcoll_name):

    if utils.is_null_or_empty(snapcoll_name):
        return (False, False, "Snapshot collection deletion failed as snapshot collection name is not present.", {})

    try:
        snapcoll_resp = client_obj.snapshot_collections.get(id=None, name=snapcoll_name)
        if utils.is_null_or_empty(snapcoll_resp):
            return (False, False, f"Snapshot collection '{snapcoll_name}' not present to delete.", {})
        else:
            client_obj.snapshot_collections.delete(id=snapcoll_resp.attrs.get("id"))
            return (True, True, f"Snapshot collection '{snapcoll_name}' deleted successfully.", {})
    except Exception as ex:
        return (False, False, f"Snapshot collection deletion failed | {ex}", {})


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
        "volcoll": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "is_external_trigger": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "vol_snap_attr_list": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "replicate_to": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "start_online": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "allow_writes": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "disable_appsync": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "snap_verify": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "skip_db_consistency_check": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "invoke_on_upstream_partner": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "agent_type": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "metadata": {
            "required": False,
            "type": "dict",
            "no_log": False
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
    required_if = [('state', 'create', ['volcoll'])]

    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    snapcoll_name = module.params["name"]
    description = module.params["description"]
    volcoll = module.params["volcoll"]
    is_external_trigger = module.params["is_external_trigger"]
    vol_snap_attr_list = module.params["vol_snap_attr_list"]
    replicate_to = module.params["replicate_to"]
    start_online = module.params["start_online"]
    allow_writes = module.params["allow_writes"]
    disable_appsync = module.params["disable_appsync"]
    snap_verify = module.params["snap_verify"]
    skip_db_consistency_check = module.params["skip_db_consistency_check"]
    invoke_on_upstream_partner = module.params["invoke_on_upstream_partner"]
    agent_type = module.params["agent_type"]
    metadata = module.params["metadata"]
    expiry_after = module.params["expiry_after"]
    force = module.params["force"]

    if (username is None or password is None or hostname is None or snapcoll_name is None):
        module.fail_json(
            msg="Missing variables: hostname, username, password and snapshot collection name is mandatory.")

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
        snapcoll_resp = client_obj.snapshot_collections.get(id=None, name=snapcoll_name)
        if utils.is_null_or_empty(snapcoll_resp) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_snapcoll(
                client_obj,
                snapcoll_name,
                description=description,
                volcoll_id=utils.get_volcoll_id(client_obj, volcoll),
                is_external_trigger=is_external_trigger,
                vol_snap_attr_list=vol_snap_attr_list,
                replicate_to=replicate_to,
                start_online=start_online,
                allow_writes=allow_writes,
                disable_appsync=disable_appsync,
                snap_verify=snap_verify,
                skip_db_consistency_check=skip_db_consistency_check,
                invoke_on_upstream_partner=invoke_on_upstream_partner,
                agent_type=agent_type,
                metadata=metadata)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_snapcoll(
                client_obj,
                snapcoll_resp,
                description=description,
                replicate_to=replicate_to,
                expiry_after=expiry_after,
                metadata=metadata,
                force=force)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_snapcoll(client_obj, snapcoll_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
