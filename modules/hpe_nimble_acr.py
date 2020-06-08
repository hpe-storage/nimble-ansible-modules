#!/usr/bin/python

# Copyright: (c) 2020, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+
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
description: "On HPE Nimble Storage Array- Create or delete ACL for volume"
module: hpe_nimble_acr

options:
    state:
        required: True
        choices:
            - present
            - absent
            - create
        type: 'str'
        description:
        - choice for ACR operation
    apply_to:
        required: False
        type: str
        default: both
        description:
        - Type of object this access control record applies to. Possible values, 'volume', 'snapshot', 'both', 'pe', 'vvol_volume', 'vvol_snapshot'.
    chap_user_name:
        required: False
        type: str
        description:
        - Name for the CHAP user.
    lun:
        required: False
        type: int
        description:
        - If this access control record applies to a regular volume, this attribute is the volume's LUN (Logical Unit Number).
          If the access protocol is iSCSI, the LUN will be 0. However, if the access protocol is Fibre Channel, the LUN will be in the range from 0 to 2047
    vol_name:
        required: False
        type: str
        description:
        - Name for the volume this access control record applies to.
    pe_ids:
        required: False
        type: list
        description:
        - List of candidate protocol endpoints that may be used to access the Virtual Volume. One of them will be selected for the access control record.
          This field is required only when creating an access control record for a Virtual Volume.
    pe_name:
        required: False
        type: str
        description:
        - Name for the protocol endpoint this access control record applies to.
    snap_name:
        required: False
        type: str
        description:
        - Name of the snapshot this access control record applies to.
    initiator_group_name:
        required: False
        type: str
        description:
        - The Initiator Group name.

extends_documentation_fragment: hpenimble
short_description: "Manage HPE Nimble Storage ACR"
version_added: "2.9"
'''

EXAMPLES = r'''

    # if state is create, then create acl for given volume ,fails if it exist or cannot create
    # if state is present, then create acl if not present ,else success
    - name: Create ACR for volume
      hpe_nimble_acr:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        vol_name: "{{ vol_name }}"
        initiator_group_name: "{{ initiator_group_name }}"
        state: "{{ state | default('present') }}" # fail if exist

    # delete the acl for a given volume name
    - name: Delete ACR for volume
      hpe_nimble_acr:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        vol_name: "{{ vol_name }}"
        state: "absent" # fail if volume does not exist

'''
RETURN = r'''
'''


from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible.module_utils.hpenimble as utils


def create_acr(
        client_obj,
        initiator_group_name,
        vol_name,
        state,
        **kwargs):

    if utils.is_null_or_empty(initiator_group_name):
        return (False, False, "ACR creation failed. No initiator_group_name provided")
    if utils.is_null_or_empty(vol_name):
        return (False, False, "ACR creation failed. No Volume name provided")

    try:
        # see if the igroup is already present
        ig_resp = client_obj.initiator_groups.get(id=None, name=initiator_group_name)
        if ig_resp is None:
            return (False, False, "Initiator Group '%s' is not present on Array" % initiator_group_name)
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if vol_resp is None:
            return (False, False, "Volume name '%s' is not present on Array" % vol_name)

        acr_resp = client_obj.access_control_records.get(id=None, vol_name=vol_name)
        if utils.is_null_or_empty(acr_resp) is False:
            changed_attrs_dict, params = utils.remove_unchanged_or_null_args(acr_resp, **kwargs)
        else:
            params = utils.remove_null_args(**kwargs)
        if acr_resp is None or acr_resp.attrs.get("initiator_group_id") != ig_resp.attrs.get("id"):
            acr_resp = client_obj.access_control_records.create(initiator_group_id=ig_resp.attrs.get("id"),
                                                                vol_id=vol_resp.attrs.get("id"),
                                                                **params)
            return (True, True, "Successfully Created ACR for volume '%s'" % vol_name)
        else:
            # check the state. if it is set to present ,we pass else if it is 'create' then we will fail
            if state == "present":
                return (True, False, "ACR is already present for volume '%s'" % vol_name)
        return (False, False, "Cannot create ACR for Volume '%s' as it is already present" % vol_name)
    except Exception as e:
        return (False, False, "ACR Creation failed | %s" % e)


def delete_acr(
        client_obj,
        vol_name):

    if utils.is_null_or_empty(vol_name):
        return (False, False, "ACR deletion failed. No Volume name Provided")

    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if vol_resp is None:
            return (False, False, "Volume name '%s' is not present on Array" % vol_name)

        acr_resp = client_obj.access_control_records.get(id=None, vol_name=vol_name)
        if acr_resp is not None:
            acr_resp = client_obj.access_control_records.delete(acr_resp.attrs.get("id"))
            return (True, True, "Successfully Deleted ACR for volume '%s'" % vol_name)
        else:
            return (True, False, "Cannot delete ACR for Volume '%s' as it is not present" % vol_name)
    except Exception as e:
        return (False, False, "ACR Deletion failed | %s" % e)


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present',
                        'absent',
                        'create'
                        ],
            "type": 'str'
        },
        "apply_to": {
            "required": False,
            "type": "str",
            "no_log": False,
            "default": "both"
        },
        "chap_user_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "lun": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "vol_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "pe_ids": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "pe_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "snap_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "initiator_group_name": {
            "required": False,
            "type": "str",
            "no_log": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    module = AnsibleModule(argument_spec=fields)
    if client is None:
        module.fail_json(msg='the python nimble_sdk module is required')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    apply_to = module.params["apply_to"]
    chap_user_name = module.params["chap_user_name"]
    lun = module.params["lun"]
    vol_name = module.params["vol_name"]
    pe_ids = module.params["pe_ids"]
    pe_name = module.params["pe_name"]
    snap_name = module.params["snap_name"]
    initiator_group_name = module.params["initiator_group_name"]

    if (username is None or password is None or hostname is None):
        module.fail_json(
            msg="Storage system IP or username or password is null")

    client_obj = client.NimOSClient(
        hostname,
        username,
        password
    )

    # defaults
    return_status = changed = False
    msg = "No Task was run"

    # States
    if state == "create" or state == "present":
        return_status, changed, msg = create_acr(
            client_obj, initiator_group_name, vol_name, state,
            apply_to=apply_to, chap_user_id=utils.get_chap_user_id(client_obj, chap_user_name), lun=lun,
            pe_ids=pe_ids, pe_name=utils.get_pe_id(client_obj, pe_name), snap_id=utils.get_snapshot_id(client_obj, snap_name))

    elif state == "absent":
        return_status, changed, msg = delete_acr(client_obj, vol_name)

    if return_status:
        module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
