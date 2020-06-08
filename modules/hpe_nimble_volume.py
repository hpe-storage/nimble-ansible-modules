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
description: "On HPE Nimble Storage Array- Create, Update, Delete Volume  Online, Offline and Clone Volume"
module: hpe_nimble_volume
options:
    state:
        description:
        - "Choice for Volume operations"
        choices:
        - present
        - absent
        - create
        - online
        - offline
        - restore
        required: True
        type: str
    name:
        required: True
        type: str
        description:
        - "Name of the Source Volume."
    size:
        type: int
        default: 100
        description:
        - "The size of the volume."
    description:
        required: False
        type: str
        default: null
        description:
        - Text description of volume.
    perfpolicy_name:
        required: False
        type: str
        default: null
        description:
        - Name of the performance policy.After creating a volume, performance policy for the volume can only be
          changed to another performance policy with same block size.
    limit:
        required: False
        type: int
        default: 100
        description:
        - Limit on the volume's mapped usage, expressed as a percentage of the volume's size
    online:
        required: False
        type: bool
        default: True
        description:
        - Online state of volume, available for host initiators to establish connections.
    owned_by_group_name:
        required: False
        type: str
        default: null
        description:
        - Name of group that currently owns the volume
    multi_initiator:
        required: False
        type: bool
        default: False
        description:
        - For iSCSI Volume Target, this flag indicates whether the volume and its snapshots can be accessed from multiple initiators at the same time.
    iscsi_target_scope:
        required: False
        type: str
        choices:
            - volume
            - group
        default: 'volume'
        description:
        - This indicates whether volume is exported under iSCSI Group Target or iSCSI Volume Target. This attribute is only meaningful to iSCSI system
    pool_name:
        required: False
        type: str
        default: null
        description:
        - Name associated with the pool in the storage pool table.
    read_only:
        required: False
        type: bool
        default: False
        description:
        - Volume is read-only.
    block_size:
        required: False
        type: int
        default: 4096
        description:
        - Size in bytes of blocks in the volume.
    clone:
        required: False
        type: bool
        default: False
        description:
        - Whether this volume is a clone.Use this attribute in combination with name and snapshot_name to create a clone by setting clone = true.
    agent_type:
        required: False
        choices:
            - none
            - smis
            - vvol
            - openstack
            - openstackv2
        type: str
        default: 'none'
        description:
        - External management agent type.
    dest_pool_name:
        required: False
        type: str
        default: null
        description:
        - Name of the destination pool where the volume is moving to.
    cache_pinned:
        required: False
        type: bool
        default: False
        description:
        - If set to true, all the contents of this volume are kept in flash cache.
    thinly_provisioned:
        required: False
        type: bool
        default: True
        description:
        - Set volume's provisioning level to thin.
    encryption_cipher:
        required: False
        choices:
            - none
            - aes_256_xts
        type: str
        default: 'none'
        description:
        - The encryption cipher of the volume.
    app_uuid:
        required: False
        type: str
        default: null
        description:
        - Application identifier of volume.
    folder_name:
        required: False
        type: str
        default: null
        description:
        - Name of the folder holding this volume.
    metadata:
        required: False
        type: dict
        default: null
        description:
        - Key-value pairs that augment an volume's attributes.
    dedupe_enabled:
        required: False
        type: bool
        default: False
        description:
        - Indicate whether dedupe is enabled.
    limit_iops:
        required: False
        type: int
        default: -1
        description:
        - IOPS limit for this volume.
    limit_mbps:
        required: False
        type: int
        default: -1
        description:
        - Throughput limit for this volume in MB/s.
    parent_vol_name:
        required: False
        type: str
        default: null
        description:
        - Name of parent volume
    snapshot_name:
        required: False
        type: str
        default: null
        description:
        - Base snapshot name. This attribute is required together with name and clone when cloning a volume with the create operation
    volcoll_name:
        required: False
        type: str
        default: null
        description:
        - Name of volume collection of which this volume is a member.
    force:
        required: False
        type: bool
        default: False
        description:
        - Forcibly offline, reduce size or change read-only status a volume.
    force_vvol:
        required: False
        type: bool
        default: False
        description:
        - Forcibly move a Virtual Volume.
    move:
        required: False
        type: bool
        default: False
        description:
        - Move a Volume to different Pool.

extends_documentation_fragment: hpenimble
short_description: "Manage HPE Nimble Storage volume"
version_added: "2.9"
'''

EXAMPLES = r'''

      # if state is create , then create a volume if not present. Fails if already present.
      # if state is "present", then create a volume if not present, But Success if it already exists
    - name: Create Volume if not present
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        state: "{{ state | default('present') }}" # fail if exist
        size: "{{ size }}"
        limit_iops: "{{ limit_iops }}"
        limit_mbps: 5000
        force: false
        metadata: "{{ metadata }}"
        description: "{{ description }}"
        name: "{{ name }}"

    - name: Changing Volume "{{ name }}" to offline state
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        state: offline
        name: "{{ name }}"

    - name: Changing Volume "{{ name }}" to online state
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        state: online
        name: "{{ name }}"

    # Create a clone from the given snapshot name.
    # if snapshot name is not provided then create a snapshot of source volume
    # clone task should only run if parent_vol_name is specified.snapshot name is optional
    - name: Let's create or refresh a clone!
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        name: "{{ name }}" # do we neeed the source vol if snapshot_name is provided?
        parent_vol_name: "{{ parent_vol_name | mandatory }}"
        snapshot_name: "{{ snapshot_name | default(None)}}"
        state: "{{ state | default('present') }}" # fail if exist
      when:
        - parent_vol_name is defined

    - name: Let's destroy myvol1 (it's not offline)
      hpe_nimble_volume:
        name: "{{ name }}"
        state: absent

    # if no snapshot_name is given then restore volume to last snapshot,fails if no snapshots exist
    # or if snapshot_name is provided then restore volume from that snapshot
    - name: Restore volume "{{ name }}".
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        name: "{{ name }}"
        snapshot_name: "{{ snapshot_name | default(None)}}"
        state: restore

    - name: Delete volume "{{ name }}" (it's not offline)
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        name: "{{ name }}"
        state: absent

    - name: Volume Move to pool
      hpe_nimble_volume:
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
        move: true
        name: "{{ name }}"
        dest_pool_name: "{{ dest_pool_name | mandatory }}"

'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
    from nimbleclient import exceptions
except ImportError:
    client = None
import ansible.module_utils.hpenimble as utils
from enum import Enum


class Vol_Operation(Enum):
    SUCCESS = 0
    ALREADY_EXISTS = -1
    FAILED = 1

# util functions

def move_volume(
        client_obj,
        vol_name,
        dest_pool_name,
        force_vvol):

    if utils.is_null_or_empty(vol_name):
        return (False, False, "Volume Move failed. Volume name is null", {})

    if utils.is_null_or_empty(dest_pool_name):
        return (False, False, "Volume Move failed. dest_pool_name is null", {})
    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if utils.is_null_or_empty(vol_resp):
            return (False, False, "Volume '%s' not present to move" % vol_name, {})

        client_obj.volumes.move(id=vol_resp.attrs.get("id"), dest_pool_id=utils.get_pool_id(client_obj, dest_pool_name), force_vvol=force_vvol)
        return (True, True, "Volume '%s' moved Successfully." % vol_resp.attrs.get("name"), {})
    except Exception as ex:
        return (False, False, "Volume Move failed | %s" % ex, {})


def update_volume(
        client_obj,
        vol_resp,
        **kwargs):

    if utils.is_null_or_empty(vol_resp):
        return (False, False, "Invalid volume to update", {})
    try:
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(vol_resp, **kwargs)

        if changed_attrs_dict.__len__() > 0:
            client_obj.volumes.update(id=vol_resp.attrs.get("id"), **params)
            return (True, True, "Volume '%s' already present. Modified the following fields:" % vol_resp.attrs.get("name"), changed_attrs_dict)
        else:
            return (True, False, "Volume '%s' already present." % vol_resp.attrs.get("name"), {})
    except Exception as ex:
        return (False, False, "Volume update failed | %s" % ex, {})


def create_volume(
        client_obj,
        vol_name,
        **kwargs):

    if utils.is_null_or_empty(vol_name):
        return (False, False, "Volume creation failed. Volume name is null", {})

    if len(vol_name) < 1 or len(vol_name) > 214:
        return (False, False, "Volume create failed. Volume name ' %s 'must be atleast 1 character and not more than 214 "
                "characters" % vol_name, {})
    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        # remove unchanged and null arguments from kwargs
        params = utils.remove_null_args(**kwargs)
        if utils.is_null_or_empty(vol_resp):
            client_obj.volumes.create(vol_name, **params)
            return (True, True, "Created volume %s successfully." % vol_name, {})
        else:
            return (False, False, "Cannot create Volume '%s' as it is already present" % vol_name, {})
    except Exception as e:
        return (False, False, "Volume creation failed | %s" % e, {})


def delete_volume(client_obj, vol_name):
    if utils.is_null_or_empty(vol_name):
        return (False, False, "Volume deletion failed. Volume name is null", {})

    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if utils.is_null_or_empty(vol_resp):
            return (False, False, "Volume '%s' not present to delete" % vol_name, {})
        else:
            # disassociate the volume from vol coll
            client_obj.volumes.update(id=vol_resp.attrs.get("id"), volcoll_id="")
            client_obj.volumes.offline(id=vol_resp.attrs.get("id"))
            client_obj.volumes.delete(id=vol_resp.attrs.get("id"))
            return (True, True, "Deleted volume %s successfully." % vol_name, {})
    except Exception as e:
        return (False, False, "Volume deletion failed | %s" % e, {})


def restore_volume(client_obj, vol_name, snapshot_name_to_restore=None):
    if utils.is_null_or_empty(vol_name):
        return (False, False, "Volume restore failed. Volume name is null", {})
    try:
        vol_resp = client_obj.volumes.get(id=None, name=vol_name)
        if utils.is_null_or_empty(vol_resp):
            return (False, False, "Volume '%s' not present to restore" % vol_name, {})

        if utils.is_null_or_empty(snapshot_name_to_restore):
            # restore the volume to the last snapshot
            snap_list_resp = client_obj.snapshots.list(vol_name=vol_name)
            if utils.is_null_or_empty(snap_list_resp):
                return (False, False, "Could not restore Volume '%s' as no snapshot is present in Source volume"
                        % vol_name, {})
            snap_resp = snap_list_resp[-1]
            snapshot_name_to_restore = snap_resp.attrs.get("name")
        else:
            # get the snapshot detail from the given source vol
            snap_resp = client_obj.snapshots.get(vol_name=vol_name, name=snapshot_name_to_restore)
            if utils.is_null_or_empty(snap_resp):
                return (False, False, "Could not restore Volume '%s' as given snapshot name '%s' is not present in Source volume"
                        % (vol_name, snapshot_name_to_restore), {})

        # offline and restore
        client_obj.volumes.offline(id=vol_resp.attrs.get("id"))
        client_obj.volumes.restore(base_snap_id=snap_resp.attrs.get("id"),
                                   id=vol_resp.attrs.get("id"))
        # bring volume online
        client_obj.volumes.online(id=vol_resp.attrs.get("id"))
        return (True, True, "Restored volume %s from snapshot '%s' successfully." % (vol_name, snapshot_name_to_restore), {})
    except Exception as e:
        return (False, False, "Volume restore failed | %s" % e, {})


def change_volume_state(
        client_obj,
        vol_name,
        online):

    if utils.is_null_or_empty(vol_name):
        return (False, False, "Change volume state failed. Volume name is null", {})
    try:
        resp = client_obj.volumes.get(id=None, name=vol_name)
        changed_attrs_dict = {}
        if utils.is_null_or_empty(resp) is False:
            if resp.attrs.get("online") == online:
                return (True, False, "Volume '%s' online state is already set to '%s'." % (vol_name, online), {})
            elif online is True:
                resp = client_obj.volumes.online(resp.attrs.get("id"))
                changed_attrs_dict['online'] = "True"
                return (True, True, "Changed volume '%s' state to Online successfully." % vol_name, changed_attrs_dict)
            elif online is False:
                resp = client_obj.volumes.offline(resp.attrs.get("id"))
                changed_attrs_dict['online'] = "False"
                return (True, True, "Changed volume '%s' state to Offline successfully." % vol_name, changed_attrs_dict)
            # elif online is True and resp.attrs.get("online") is True:
            #     return (True, False, "Volume '%s' state is already set to Online." % vol_name, {})
        else:
            return (False, False, "Could not find Volume '%s'" % vol_name, {})
    except Exception as e:
        return (False, False, "Change Volume State failed | %s" % e, {})


# given a snapshot name,create a clone.
# return code
# SUCCESS = 0
# ALREADY_EXISTS = -1
# FAILED = 1
def create_clone_from_snapshot(
        client_obj,
        snap_list_resp,
        vol_name,
        snapshot_name_to_clone,
        state):
    # if client_obj is None or not snap_list_resp or snap_list_resp is None or parent_vol_name is None:
    if (utils.is_null_or_empty(client_obj)
        or utils.is_null_or_empty(vol_name)
            or utils.is_null_or_empty(snap_list_resp)
            or utils.is_null_or_empty(snapshot_name_to_clone)):
        return (False, "create_clone_from_snapshot failed as valid args not provided")
    try:
        # to_return = Vol_Operation.FAILED  # assume failed
        # find the snapshot from snapshot list
        for snap_obj in snap_list_resp:
            if snap_obj.attrs.get("name") == snapshot_name_to_clone:
                # create
                resp = client_obj.volumes.create(name=vol_name,
                                                 base_snap_id=snap_obj.attrs.get("id"),
                                                 clone=True)
                if utils.is_null_or_empty(resp) is False:
                    return (Vol_Operation.SUCCESS, "%s" % vol_name)
        return (Vol_Operation.FAILED)
    except exceptions.NimOSAPIError as ex:
        if "SM_eexist" in str(ex):
            # check the state. if it set to present then return true
            if state == "present":
                return (Vol_Operation.ALREADY_EXISTS, "Destination Cloned Volume '%s' is already present" % (vol_name))
            else:
                return (Vol_Operation.FAILED, "create_clone_from_snapshot failed as Dest clone volume '%s' already exist| %s" % (vol_name, ex))
    except Exception as e:
        return (Vol_Operation.FAILED, "create_clone_from_snapshot failed | %s" % e)


def clone_volume(
        client_obj,
        parent_vol_name,
        state,
        vol_name=None,
        snapshot_name_to_clone=None):

    if utils.is_null_or_empty(vol_name):
        return (False, False, "Clone operation failed. Clone Volume name is not present.", {})
    # this function will handle 2 scenario.
    # If snapshot name is given. we try to clone from that else
    # we first create a snapshot of source volume and then
    # clone from the snapshot
    try:
        if utils.is_null_or_empty(snapshot_name_to_clone):
            if utils.is_null_or_empty(parent_vol_name):
                return (False, False, "Clone operation failed. Parent Volume name is not present.", {})
            # get the vol id
            vol_resp = client_obj.volumes.get(name=parent_vol_name)
            if utils.is_null_or_empty(vol_resp):
                return (False, False, "Clone operation failed. Parent Volume name is not present.", {})
            else:
                # create a temp snapshot
                snapshot_name_to_clone = utils.get_unique_string("ansible-snapshot")
                snap_resp = client_obj.snapshots.create(name=snapshot_name_to_clone,
                                                        vol_id=vol_resp.attrs.get("id"),
                                                        description="created by ansible",
                                                        online=False,
                                                        writable=False)
                if utils.is_null_or_empty(snap_resp):
                    return (False, False, "Clone Operation Failed. Could not create a snapshot from source volume", {})
                # create clone
                clonevol_resp, msg = create_clone_from_snapshot(client_obj, [snap_resp], vol_name, snapshot_name_to_clone, state)
                if clonevol_resp == Vol_Operation.ALREADY_EXISTS or clonevol_resp == Vol_Operation.FAILED:
                    # remove the snapshot
                    client_obj.snapshots.delete(id=snap_resp.attrs.get("id"))
        else:
            # get the snapshot detail from the given source vol
            snap_list_resp = client_obj.snapshots.list(vol_name=parent_vol_name, name=snapshot_name_to_clone)
            if utils.is_null_or_empty(snap_list_resp):
                return (False, False, "Could not create clone Volume '%s' as given snapshot name '%s' is not present in Parent volume"
                        % (vol_name, snapshot_name_to_clone), {})
            # create clone
            clonevol_resp, msg = create_clone_from_snapshot(client_obj, snap_list_resp, vol_name, snapshot_name_to_clone, state)

        if clonevol_resp is Vol_Operation.SUCCESS:
            return (True, True, "Successfully Created Cloned volume '%s'" % msg, {})
        elif clonevol_resp is Vol_Operation.FAILED:
            return (False, False, "Failed to Clone Volume. Msg: '%s'" % msg, {})
        elif clonevol_resp == Vol_Operation.ALREADY_EXISTS:
            return (True, False, " '%s'" % msg, {})
    except Exception as e:
        return (False, False, "clone_volume Operation Failed | %s" % e, {})


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present',
                        'absent',
                        'create',
                        'online',
                        'offline',
                        'restore'
                        ],
            "type": 'str'
        },
        "name": {
            "required": True,
            "type": "str"
        },
        "size": {
            "type": "int",
            "default": 100
        },
        "description": {
            "required": False,
            "type": "str",
            "default": None
        },
        "perfpolicy_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "limit": {
            "required": False,
            "type": "int",
        },
        "online": {
            "required": False,
            "type": "bool",
            "default": True
        },
        "owned_by_group_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "multi_initiator": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "iscsi_target_scope": {
            "required": False,
            "choices": ['volume', 'group'],
            "type": "str",
            "default": 'volume'
        },
        "pool_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "read_only": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "block_size": {
            "required": False,
            "type": "int",
            "default": 4096
        },
        "clone": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "agent_type": {
            "required": False,
            "choices": ['none', 'smis', 'vvol', 'openstack', 'openstackv2'],
            "type": "str",
            "default": 'none'
        },
        "dest_pool_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "cache_pinned": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "thinly_provisioned": {
            "required": False,
            "type": "bool",
            "default": True
        },
        "encryption_cipher": {
            "required": False,
            "choices": ['none', 'aes_256_xts'],
            "type": "str",
            "default": 'none'
        },
        "app_uuid": {
            "required": False,
            "type": "str",
            "default": None
        },
        "folder_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "dedupe_enabled": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "limit_iops": {
            "required": False,
            "type": "int"
        },
        "limit_mbps": {
            "required": False,
            "type": "int"
        },
        "parent_vol_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "snapshot_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "volcoll_name": {
            "required": False,
            "type": "str",
            "default": None
        },
        "metadata": {
            "required": False,
            "type": "dict",
            "default": None
        },
        "force": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "force_vvol": {
            "required": False,
            "type": "bool",
            "default": False
        },
        "move": {
            "required": False,
            "type": "bool",
            "default": False
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    required_if = [('state', 'restore', ['snapshot_name'])]

    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='the python nimble_sdk module is required')

    state = module.params["state"]
    vol_name = module.params["name"]
    size = module.params["size"]
    description = module.params["description"]
    perfpolicy_name = module.params["perfpolicy_name"]
    limit = module.params["limit"]
    online = module.params["online"]
    owned_by_group_name = module.params["owned_by_group_name"]
    multi_initiator = module.params["multi_initiator"]
    iscsi_target_scope = module.params["iscsi_target_scope"]
    pool_name = module.params["pool_name"]
    read_only = module.params["read_only"]
    block_size = module.params["block_size"]
    clone = module.params["clone"]
    agent_type = module.params["agent_type"]
    dest_pool_name = module.params["dest_pool_name"]
    cache_pinned = module.params["cache_pinned"]
    thinly_provisioned = module.params["thinly_provisioned"]
    encryption_cipher = module.params["encryption_cipher"]
    app_uuid = module.params["app_uuid"]
    folder_name = module.params["folder_name"]
    dedupe_enabled = module.params["dedupe_enabled"]
    limit_iops = module.params["limit_iops"]
    limit_mbps = module.params["limit_mbps"]
    parent_vol_name = module.params["parent_vol_name"]  # used for cloning
    snapshot_name = module.params["snapshot_name"]
    volcoll_name = module.params["volcoll_name"]
    metadata = module.params["metadata"]
    force = module.params["force"]
    force_vvol = module.params["force_vvol"]
    move = module.params["move"]
    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]

    if (username is None or password is None or hostname is None):
        module.fail_json(msg="Volume creation failed. Storage system IP or username or password is null")

    client_obj = client.NimOSClient(
        hostname,
        username,
        password
    )
    # defaults
    return_status = changed = False
    msg = "No Task was run"

    # States
    if move is True and state == "present":
        if utils.is_null_or_empty(dest_pool_name) is False:
            return_status, changed, msg, changed_attrs_dict = move_volume(client_obj, vol_name, dest_pool_name, force_vvol)
        else:
            module.fail_json(msg="Volume Move failed. dest_pool_name is null")

    elif state == "create" or state == "present":
        # state create/present can be provided for creating a new volume or
        # creating a clone from source volume
        if parent_vol_name is not None:
            return_status, changed, msg, changed_attrs_dict = clone_volume(
                client_obj, parent_vol_name, state,
                vol_name, snapshot_name)
        else:
            if utils.is_null_or_empty(vol_name):
                return_status = changed = False
                msg = "Volume creation failed. Volume name is null"
            else:
                vol_resp = client_obj.volumes.get(id=None, name=vol_name)
                if utils.is_null_or_empty(vol_resp) or state == "create":
                    return_status, changed, msg, changed_attrs_dict = create_volume(
                        client_obj, vol_name, perfpolicy_id=utils.get_perfpolicy_id(client_obj, perfpolicy_name), size=size, description=description,
                        limit=limit, online=online, owned_by_group_id=utils.get_owned_by_group_id(client_obj, owned_by_group_name), multi_initiator=multi_initiator,
                        pool_id=utils.get_pool_id(client_obj, pool_name), iscsi_target_scope=iscsi_target_scope, read_only=read_only, block_size=block_size,
                        clone=clone, agent_type=agent_type, dest_pool_n=dest_pool_name,
                        metadata=metadata, cache_pinned=cache_pinned, thinly_provisioned=thinly_provisioned, encryption_cipher=encryption_cipher,
                        app_uuid=app_uuid, folder_id=utils.get_folder_id(client_obj, folder_name), dedupe_enabled=dedupe_enabled, limit_iops=limit_iops,
                        limit_mbps=limit_mbps)
                else:
                    # if utils.is_null_or_empty(dest_pool_name) is False:
                    #     # it is a move operation
                    #     return_status, changed, msg, changed_attrs_dict = move_volume(
                    #         client_obj, vol_resp, dest_pool_name, force_vvol)
                    #     if return_status is False:
                    #         module.fail_json(return_status=return_status, changed=changed, msg=msg)
                    #     vol_resp = client_obj.volumes.get(id=None, name=vol_name)

                    # if we are here it means volume is already present. hence issue update call
                    return_status, changed, msg, changed_attrs_dict = update_volume(
                        client_obj, vol_resp, size=size, perfpolicy_id=utils.get_perfpolicy_id(client_obj, perfpolicy_name), description=description,
                        limit=limit, online=online, owned_by_group_id=utils.get_owned_by_group_id(client_obj, owned_by_group_name), multi_initiator=multi_initiator,
                        iscsi_target_scope=iscsi_target_scope, read_only=read_only, block_size=block_size, clone=clone, agent_type=agent_type,
                        volcoll_id=utils.get_volcoll_id(client_obj, volcoll_name), metadata=metadata,
                        cache_pinned=cache_pinned, thinly_provisioned=thinly_provisioned, app_uuid=app_uuid, folder_id=utils.get_folder_id(client_obj, folder_name),
                        dedupe_enabled=dedupe_enabled, limit_iops=limit_iops, limit_mbps=limit_mbps, force=force)

    elif state == "offline":
        return_status, changed, msg, changed_attrs_dict = change_volume_state(client_obj, vol_name, False)

    elif state == "online":
        return_status, changed, msg, changed_attrs_dict = change_volume_state(client_obj, vol_name, True)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_volume(client_obj, vol_name)

    elif state == "restore":
        return_status, changed, msg, changed_attrs_dict = restore_volume(client_obj, vol_name, snapshot_name)

    if return_status:
        if not utils.is_null_or_empty(changed_attrs_dict) and changed_attrs_dict.__len__() > 0:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, message=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
