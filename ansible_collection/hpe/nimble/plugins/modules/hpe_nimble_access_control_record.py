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
  - Alok Ranjan (@ranjanal)
description: On HPE Nimble Storage array - Create or delete access control record for volume.
module: hpe_nimble_access_control_record
options:
  apply_to:
    required: False
    choices:
    - volume
    - snapshot
    - both
    - pe
    - vvol_volume
    - vvol_snapshot
    type: str
    default: both
    description:
    - Type of object this access control record applies to.
  chap_user:
    required: False
    type: str
    description:
    - Name for the CHAP user.
  initiator_group:
    required: False
    type: str
    description:
    - The Initiator group name.
  lun:
    required: False
    type: int
    description:
    - If this access control record applies to a regular volume, this attribute is the volume's LUN Logical Unit Number.
    - If the access protocol is iSCSI, the LUN will be 0. However, if the access protocol is fibre channel, the LUN will be in the range from 0 to 2047.
  pe_ids:
    required: False
    type: list
    description:
    - List of candidate protocol endpoints that may be used to access the Virtual volume. One of them will be selected for the access control record.
    - This field is required only when creating an access control record for a virtual volume.
  protocol_endpoint:
    required: False
    type: str
    description:
    - Name for the protocol endpoint this access control record applies to.
  snapshot:
    required: False
    type: str
    description:
    - Name of the snapshot this access control record applies to. If this record applies to a VVol snapshot, this attribute is required.
      Otherwise, this attribute is not meaningful and should not be specified.
  state:
    required: True
    choices:
    - present
    - absent
    - create
    type: str
    description:
    - Choice for access control record operation.
  volume:
    required: False
    type: str
    description:
    - Name for the volume this access control record applies to.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage access control records.
version_added: 2.9
'''

EXAMPLES = r'''

# If state is "create", create access control record for given volume, fails if it exist.
# If state is "present", create access control record if not already present.
- name: Create access control record for volume
  hpe_nimble_access_control_record:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    volume: "{{ volume }}"
    initiator_group: "{{ initiator_group }}"
    state: "{{ state | default('present') }}"

# Delete the access control record for a given volume name
- name: Delete access control record for volume
  hpe_nimble_access_control_record:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    volume: "{{ volume }}"
    initiator_group: "{{ initiator_group }}"
    state: "absent" # fail if volume does not exist

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils

def create_acr(
        client_obj,
        state,
        volume,
        **kwargs):

    try:
        params = utils.remove_null_args(**kwargs)
        # check if params has atleast 2 params. vol_id is mandatory along with any of below.
        if params.__len__() < 2:
            return (False, False, "Access control record creation failed. Please provide one of them: initiator_group or snapshot or protocol endpoint.")

        if 'snap_id' in params:
            resp = client_obj.snapshots.get(vol_name=volume, id=params['snap_id'])
            obj_type = 'snapshot'
        elif 'pe_id' in params:
            resp = client_obj.protocol_endpoints.get(id=params['pe_id'])
            obj_type = 'protocol endpoint'
        elif 'initiator_group_id' in params:
            resp = client_obj.initiator_groups.get(id=params['initiator_group_id'])
            obj_type = 'initiator group'
        client_obj.access_control_records.create(**params)

        return (True, True, f"Successfully created access control record for {obj_type} '{resp.attrs.get('name')}' associated with volume '{volume}'.")
    except Exception as ex:
        if 'SM_eexist' in str(ex):
            msg = f"Access control record is already present for {obj_type} '{resp.attrs.get('name')}' associated with volume '{volume}'."
            if state == "present":
                return (True, False, msg)
            else:
                return (False, False, msg)
        return (False, False, f"Access control record creation failed | {ex}")


def delete_acr(
        client_obj,
        volume,
        **kwargs):

    if utils.is_null_or_empty(volume):
        return (False, False, "Access control record deletion failed. No volume name provided.")
    params = utils.remove_null_args(**kwargs)

    if params.__len__() != 1:
        return (False, False, "Access control record deletion failed. Please provide one of them: initiator_group or snapshot or protocol endpoint.")

    try:
        vol_resp = client_obj.volumes.get(id=None, name=volume)
        if vol_resp is None:
            return (False, False, f"Volume name '{volume}' is not present on array.")
        acr_resp = client_obj.access_control_records.get(vol_name=volume, **params)
        if acr_resp is not None:
            client_obj.access_control_records.delete(acr_resp.attrs.get("id"))
            return (True, True, f"Successfully deleted access control record associated with volume '{volume}' for {params}.")
        else:
            return (True, False, f"No access control record associated with volume '{volume}' for {params} found.")
    except Exception as ex:
        return (False, False, f"Access control record deletion failed | {ex}")


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'create'],
            "type": "str"
        },
        "apply_to": {
            "required": False,
            "choices": ['volume', 'snapshot', 'both', 'pe', 'vvol_volume', 'vvol_snapshot'],
            "type": "str",
            "no_log": False
        },
        "chap_user": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "lun": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "volume": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "pe_ids": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "protocol_endpoint": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "snapshot": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "initiator_group": {
            "required": False,
            "type": "str",
            "no_log": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    required_if = [('state', 'absent', ['volume'])]

    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    apply_to = module.params["apply_to"]
    chap_user = module.params["chap_user"]
    lun = module.params["lun"]
    volume = module.params["volume"]
    pe_ids = module.params["pe_ids"]
    protocol_endpoint = module.params["protocol_endpoint"]
    snapshot = module.params["snapshot"]
    initiator_group = module.params["initiator_group"]

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
    if state == "create" or state == "present":
        return_status, changed, msg = create_acr(
            client_obj,
            state,
            volume,
            apply_to=apply_to,
            chap_user_id=utils.get_chap_user_id(client_obj, chap_user),
            lun=lun,
            pe_id=utils.get_pe_id(client_obj, protocol_endpoint),
            snap_id=utils.get_snapshot_id(volume, snapshot),
            initiator_group_id=utils.get_initiator_group_id(client_obj, initiator_group),
            vol_id=utils.get_vol_id(client_obj, volume),
            pe_ids=pe_ids)

    elif state == "absent":
        return_status, changed, msg = delete_acr(
            client_obj,
            volume,
            initiator_group_name=initiator_group,
            pe_name=protocol_endpoint,
            snap_name=snapshot)

    if return_status:
        module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
