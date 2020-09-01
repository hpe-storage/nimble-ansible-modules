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
description: Manage access control records on HPE Nimble Storage group.
module: hpe_nimble_access_control_record
options:
  apply_to:
    required: False
    choices:
    - volume
    - snapshot
    - both
    type: str
    description:
    - Type of object this access control record applies to.
  chap_user:
    required: False
    type: str
    description:
    - Name for the CHAP user.
  initiator_group:
    required: True
    type: str
    description:
    - The Initiator group name.
  lun:
    required: False
    type: int
    description:
    - If this access control record applies to a regular volume, this attribute is the volume's LUN Logical Unit Number.
    - If the access protocol is iSCSI, the LUN will be 0. However, if the access protocol is fibre channel, the LUN will be in the range from 0 to 2047.
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
    required: True
    type: str
    description:
    - Name for the volume this access control record applies to.
extends_documentation_fragment: hpe.nimble.hpe_nimble
short_description: Manage HPE Nimble Storage access control records.
version_added: "2.9.0"
'''

EXAMPLES = r'''

# If state is "create", create access control record for given volume, fails if it exist.
# if state is present, create access control record if not already present.
- name: Create access control record for volume
  hpe_nimble_access_control_record:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    volume: "{{ volume }}"
    initiator_group: "{{ initiator_group }}"
    state: "{{ state | default('present') }}"

# Delete the access control record for a given volume name
- name: Delete access control record for volume
  hpe_nimble_access_control_record:
    host: "{{ host }}"
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
        initiator_group,
        volume,
        **kwargs):

    if utils.is_null_or_empty(initiator_group):
        return (False, False, "Access control record creation failed. No initiator group provided.")
    if utils.is_null_or_empty(volume):
        return (False, False, "Access control record creation failed. No volume name provided.")

    try:
        # see if the igroup is already present
        ig_resp = client_obj.initiator_groups.get(id=None, name=initiator_group)
        if ig_resp is None:
            return (False, False, f"Initiator Group '{initiator_group}' is not present on array.")
        vol_resp = client_obj.volumes.get(id=None, name=volume)
        if vol_resp is None:
            return (False, False, f"Volume name '{volume}' is not present on array.")

        acr_resp = client_obj.access_control_records.get(vol_name=volume, initiator_group_name=initiator_group, apply_to=kwargs['apply_to'])
        if utils.is_null_or_empty(acr_resp) is False:
            changed_attrs_dict, params = utils.remove_unchanged_or_null_args(acr_resp, **kwargs)
        else:
            params = utils.remove_null_args(**kwargs)
        if acr_resp is None or changed_attrs_dict.__len__() > 0:
            acr_resp = client_obj.access_control_records.create(initiator_group_id=ig_resp.attrs.get("id"),
                                                                vol_id=vol_resp.attrs.get("id"),
                                                                **params)
            params['volume'] = volume
            params['initiator_group'] = initiator_group
            return (True, True, f"Successfully created access control record with attributes: {params}.")
        else:
            # if state is set to present, we pass
            if state == "present":
                return (True, False, f"Access control record for volume '{volume}' with initiator group '{initiator_group}' is already present.")
        return (False, False, f"Access control record for volume '{volume}' with initiator group '{initiator_group}' cannot "
                "be created as it is already present.")
    except Exception as ex:
        return (False, False, f"Access control record creation failed | {ex}")


def delete_acr(
        client_obj,
        initiator_group,
        volume,
        **kwargs):

    if utils.is_null_or_empty(initiator_group):
        return (False, False, "Access control record deletion failed. No initiator group provided.")
    if utils.is_null_or_empty(volume):
        return (False, False, "Access control record deletion failed. No volume provided.")
    params = utils.remove_null_args(**kwargs)

    try:
        acr_list_resp = client_obj.access_control_records.list(vol_name=volume, initiator_group_name=initiator_group, **params)
        if acr_list_resp is not None and acr_list_resp.__len__() > 0:
            for acr_resp in acr_list_resp:
                client_obj.access_control_records.delete(acr_resp.attrs.get("id"))
            return (True, True, f"Successfully deleted access control record for initiator group '{initiator_group}' associated with volume '{volume}'.")
        else:
            return (True, False, f"No access control record for initiator group '{initiator_group}' associated with volume '{volume}' found.")
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
            "choices": ['volume', 'snapshot', 'both'],
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
        "initiator_group": {
            "required": True,
            "type": "str",
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
    apply_to = module.params["apply_to"]
    chap_user = module.params["chap_user"]
    lun = module.params["lun"]
    volume = module.params["volume"]
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
            initiator_group,
            volume,
            apply_to=apply_to,
            chap_user_id=utils.get_chap_user_id(client_obj, chap_user),
            lun=lun)

    elif state == "absent":
        return_status, changed, msg = delete_acr(
            client_obj,
            initiator_group,
            volume,
            chap_user=chap_user)

    if return_status:
        module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
