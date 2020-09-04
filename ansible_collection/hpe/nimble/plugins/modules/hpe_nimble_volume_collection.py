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
description: Manage volume collections on HPE Nimble Storage group.
module: hpe_nimble_volume_collection
options:
  abort_handover:
    required: False
    type: bool
    description:
    - Abort in-progress handover. If for some reason a previously invoked handover request is unable to complete, this action can be used to cancel it.
      This operation is not supported for synchronous replication volume collections.
  agent_hostname:
    required: False
    type: str
    description:
    - Generic backup agent hostname.
  agent_password:
    required: False
    type: str
    description:
    - Generic backup agent password.
  agent_username:
    required: False
    type: str
    description:
    - Generic backup agent username.
  app_cluster:
    required: False
    type: str
    description:
    - If the application is running within a Windows cluster environment, this is the cluster name.
  app_id:
    required: False
    choices:
    - inval
    - exchange
    - exchange_dag
    - hyperv
    - sql2005
    - sql2008
    - sql2012
    - sql2014
    - sql2016
    - sql2017
    type: str
    description:
    - Application ID running on the server.
  app_server:
    required: False
    type: str
    description:
    - Application server hostname.
  app_service:
    required: False
    type: str
    description:
    - If the application is running within a windows cluster environment then this is the instance name of the service running within the cluster environment.
  app_sync:
    choices:
    - none
    - vss
    - vmware
    - generic
    required: False
    type: str
    description:
    - Application synchronization.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing volume collection.
  demote:
    required: False
    type: bool
    description:
    - Release ownership of the specified volume collection. The volumes associated with the volume collection will be set to offline and
      a snapshot will be created, then full control over the volume collection will be transferred to the new owner. This option can be used
      following a promote to revert the volume collection back to its prior configured state. This operation does not alter the configuration on
      the new owner itself, but does require the new owner to be running in order to obtain its identity information. This operation is not supported
      for synchronous replication volume collections.
  description:
    required: False
    type: str
    description:
    - Text description of volume collection.
  handover:
    required: False
    type: bool
    description:
    - Gracefully transfer ownership of the specified volume collection. This action can be used to pass control of the volume collection
      to the downstream replication partner. Ownership and full control over the volume collection will be given to the downstream replication
      partner. The volumes associated with the volume collection will be set to offline prior to the final snapshot being taken and replicated,
      thus ensuring full data synchronization as part of the transfer. By default, the new owner will automatically begin replicating the volume
      collection back to this node when the handover completes.
  invoke_on_upstream_partner:
    required: False
    type: bool
    description:
    - Invoke handover request on upstream partner. This operation is not supported for synchronous replication volume vollections.
  is_standalone_volcoll:
    required: False
    type: bool
    default: False
    description:
    - Indicates whether this is a standalone volume collection.
  metadata:
    required: False
    type: dict
    description:
    - User defined key-value pairs that augment a volume collection attributes. List of key-value pairs. Keys must be unique and non-empty.
      When creating an object, values must be non-empty. When updating an object, an empty value causes the corresponding key to be removed.
  name:
    required: True
    type: str
    description:
    - Name of volume collection.
  no_reverse:
    required: False
    type: bool
    default: False
    description:
    - Do not automatically reverse direction of replication.
      Using this argument will prevent the new owner from automatically replicating the volume collection to this node when the handover completes.
  override_upstream_down:
    required: False
    type: bool
    description:
    - Allow the handover request to proceed even if upstream array is down. The default behavior is to return an error when upstream is down.
      This option is applicable for synchronous replication only.
  promote:
    required: False
    type: bool
    description:
    - Take ownership of the specified volume collection. The volumes associated with the volume collection will be set to online and be
      available for reading and writing. Replication will be disabled on the affected schedules and must be re-configured if desired. Snapshot
      retention for the affected schedules will be set to the greater of the current local or replica retention values. This operation is not
      supported for synchronous replication volume collections.
  prot_template:
    required: False
    type: str
    description:
    - Name of the protection template whose attributes will be used to create this volume collection.
      This attribute is only used for input when creating a volume collection and is not outputed.
  replication_partner:
    required: False
    type: str
    description:
    - Name of the new volume collection owner.
  replication_type:
    choices:
    - periodic_snapshot
    - synchronous
    required: False
    type: str
    description:
    - Type of replication configured for the volume collection.
  state:
    required: True
    choices:
    - present
    - absent
    - create
    type: str
    description:
    - Choice for volume collection operations.
  validate:
    required: False
    type: bool
    description:
    - Validate a volume collection with either Microsoft VSS or VMware application synchronization.
  vcenter_hostname:
    required: False
    type: str
    description:
    - VMware vCenter hostname.
  vcenter_username:
    required: False
    type: str
    description:
    - Application VMware vCenter username. String of up to 80 alphanumeric characters, beginning with a letter.
      It can include ampersand (@), backslash (\), dash (-), period (.), and underscore (_).
  vcenter_password:
    required: False
    type: str
    description:
    - Application VMware vCenter password. A password with few constraints.
extends_documentation_fragment: hpe.nimble.hpe_nimble
short_description: Manage HPE Nimble Storage volume collections.
version_added: "2.9.0"
'''

EXAMPLES = r'''

# if state is create , then create a volcoll if not present. Fails if already present.
# if state is present, then create a volcoll if not present. Succeed if it already exists.
- name: Create volume collection if not present
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    description: "{{ description | default(None)}}"
    state: "{{ state | default('present') }}"

- name: Delete volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: absent

- name: Promote volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    promote: True

- name: Demote volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    demote: True

- name: Handover volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    handover: True

- name: Abort handover volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    abort_handover: True

- name: Validate volume collection
  hpe_nimble_volume_collection:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: present
    validate: True

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils


def create_volcoll(
        client_obj,
        volcoll_name,
        **kwargs):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Create volume collection failed as volume collection is not present.", {})
    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp):
            params = utils.remove_null_args(**kwargs)
            volcoll_resp = client_obj.volume_collections.create(name=volcoll_name, **params)
            return (True, True, f"Created volume collection '{volcoll_name}' successfully.", {})
        else:
            return (False, False, f"Volume collection '{volcoll_name}' cannot be created as it is already present.", {})
    except Exception as ex:
        return (False, False, f"Volume collection creation failed | {ex}", {})


def update_volcoll(
        client_obj,
        volcoll_resp,
        **kwargs):

    if utils.is_null_or_empty(volcoll_resp):
        return (False, False, "Update volume collection failed as volume collection is not present.", {})
    try:
        volcoll_name = volcoll_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(volcoll_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            volcoll_resp = client_obj.volume_collections.update(id=volcoll_resp.attrs.get("id"), **params)
            return (True, True, f"Volume collection '{volcoll_name}' already present. Modified the following fields :", changed_attrs_dict)
        else:
            return (True, False, f"Volume collection '{volcoll_name}' already present.", {})
    except Exception as ex:
        return (False, False, f"Volume collection update failed | {ex}", {})


def delete_volcoll(client_obj, volcoll_name):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Delete volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present to delete.", {})
        else:

            client_obj.volume_collections.delete(id=volcoll_resp.attrs.get("id"))
            return (True, True, f"Deleted volume collection '{volcoll_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Volume collection deletion failed | {ex}", {})


def promote_volcoll(client_obj, volcoll_name):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Promote volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present to promote.", {})
        else:
            client_obj.volume_collections.promote(id=volcoll_resp.attrs.get("id"))
            return (True, True, f"Promoted volume collection '{volcoll_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Promote volume collection failed | {ex}", {})


def demote_volcoll(
        client_obj,
        volcoll_name,
        **kwargs):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Demote volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        params = utils.remove_null_args(**kwargs)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present to demote.", {})
        else:
            client_obj.volume_collections.demote(id=volcoll_resp.attrs.get("id"), **params)
            return (True, True, f"Demoted volume collection '{volcoll_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Demote volume collection failed | {ex}", {})


def handover_volcoll(
        client_obj,
        volcoll_name,
        **kwargs):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Handover of volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        params = utils.remove_null_args(**kwargs)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present for handover.", {})
        else:
            client_obj.volume_collections.handover(id=volcoll_resp.attrs.get("id"), **params)
            return (True, True, f"Handover of volume collection '{volcoll_name}' done successfully.", {})
    except Exception as ex:
        return (False, False, f"Handover of volume collection failed | {ex}", {})


def abort_handover_volcoll(
        client_obj,
        volcoll_name):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Abort handover of volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present for abort handover.", {})
        else:
            client_obj.volume_collections.abort_handover(id=volcoll_resp.attrs.get("id"))
            return (True, True, f"Abort handover of volume collection '{volcoll_name}' done successfully.", {})
    except Exception as ex:
        return (False, False, f"Abort handover of volume collection failed | {ex}", {})


def validate_volcoll(
        client_obj,
        volcoll_name):

    if utils.is_null_or_empty(volcoll_name):
        return (False, False, "Validate volume collection failed as volume collection name is null.", {})

    try:
        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp):
            return (False, False, f"Volume collection '{volcoll_name}' not present for validation.", {})
        else:
            client_obj.volume_collections.validate(id=volcoll_resp.attrs.get("id"))
            return (True, False, f"Validation of volume collection '{volcoll_name}' done successfully.", {})
    except Exception as ex:
        return (False, False, f"Validation of volume collection failed | {ex}", {})


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
        "prot_template": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "name": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "change_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "description": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "replication_type": {
            "choices": ['periodic_snapshot', 'synchronous'],
            "required": False,
            "type": "str",
            "no_log": False
        },
        "app_sync": {
            "choices": ['none', 'vss', 'vmware', 'generic'],
            "required": False,
            "type": "str",
            "no_log": False
        },
        "app_server": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "app_id": {
            "required": False,
            "choices": ['inval', 'exchange', 'exchange_dag', 'hyperv', 'sql2005', 'sql2008', 'sql2012', 'sql2014', 'sql2016', 'sql2017'],
            "type": "str",
            "no_log": False
        },
        "app_cluster": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "app_service": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "vcenter_hostname": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "vcenter_username": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "vcenter_password": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "agent_hostname": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "agent_username": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "agent_password": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "is_standalone_volcoll": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "metadata": {
            "required": False,
            "type": "dict",
            "no_log": False
        },
        "promote": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "demote": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "handover": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "abort_handover": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "validate": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "replication_partner": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "invoke_on_upstream_partner": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "no_reverse": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "override_upstream_down": {
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
    prot_template = module.params["prot_template"]
    volcoll_name = module.params["name"]
    change_name = module.params["change_name"]
    description = module.params["description"]
    replication_type = module.params["replication_type"]
    app_sync = module.params["app_sync"]
    app_server = module.params["app_server"]
    app_id = module.params["app_id"]
    app_cluster = module.params["app_cluster"]
    app_service = module.params["app_service"]
    vcenter_hostname = module.params["vcenter_hostname"]
    vcenter_username = module.params["vcenter_username"]
    vcenter_password = module.params["vcenter_password"]
    agent_hostname = module.params["agent_hostname"]
    agent_username = module.params["agent_username"]
    agent_password = module.params["agent_password"]
    is_standalone_volcoll = module.params["is_standalone_volcoll"]
    metadata = module.params["metadata"]
    promote = module.params["promote"]
    demote = module.params["demote"]
    handover = module.params["handover"]
    abort_handover = module.params["abort_handover"]
    validate = module.params["validate"]
    replication_partner = module.params["replication_partner"]
    invoke_on_upstream_partner = module.params["invoke_on_upstream_partner"]
    no_reverse = module.params["no_reverse"]
    override_upstream_down = module.params["override_upstream_down"]

    if (username is None or password is None or hostname is None):
        module.fail_json(msg="Missing variables: hostname, username and password is mandatory.")

    client_obj = client.NimOSClient(
        hostname,
        username,
        password
    )
    # defaults
    return_status = changed = False
    msg = "No task to run."

    # States.
    if state == 'present' and promote is True:
        return_status, changed, msg, changed_attrs_dict = promote_volcoll(client_obj, volcoll_name)

    elif state == 'present' and demote is True:
        return_status, changed, msg, changed_attrs_dict = demote_volcoll(
            client_obj,
            volcoll_name,
            invoke_on_upstream_partner=invoke_on_upstream_partner,
            replication_partner_id=utils.get_replication_partner_id(client_obj, replication_partner))

    elif state == 'present' and handover is True:
        return_status, changed, msg, changed_attrs_dict = handover_volcoll(
            client_obj,
            volcoll_name,
            invoke_on_upstream_partner,
            no_reverse,
            override_upstream_down,
            replication_partner_id=utils.get_replication_partner_id(client_obj, replication_partner))

    elif state == 'present' and abort_handover is True:
        return_status, changed, msg, changed_attrs_dict = abort_handover_volcoll(client_obj, volcoll_name)

    elif state == 'present' and validate is True:
        return_status, changed, msg, changed_attrs_dict = validate_volcoll(client_obj, volcoll_name)

    elif ((promote is None or promote is False)
          and (demote is None or demote is False)
          and (abort_handover is None or abort_handover is False)
          and (handover is None or handover is False)
          and (validate is None or validate is False)
          and (state == "create" or state == "present")):

        volcoll_resp = client_obj.volume_collections.get(id=None, name=volcoll_name)
        if utils.is_null_or_empty(volcoll_resp) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_volcoll(
                client_obj,
                volcoll_name,
                prottmpl_id=utils.get_prottmpl_id(client_obj, prot_template),
                description=description,
                replication_type=replication_type,
                app_sync=app_sync,
                app_server=app_server,
                app_id=app_id,
                app_cluster=app_cluster,
                app_service=app_service,
                vcenter_hostname=vcenter_hostname,
                vcenter_username=vcenter_username,
                vcenter_password=vcenter_password,
                agent_hostname=agent_hostname,
                agent_username=agent_username,
                agent_password=agent_password,
                is_standalone_volcoll=is_standalone_volcoll,
                metadata=metadata)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_volcoll(
                client_obj,
                volcoll_resp,
                name=change_name,
                description=description,
                app_sync=app_sync,
                app_server=app_server,
                app_id=app_id,
                app_cluster=app_cluster,
                app_service=app_service,
                vcenter_hostname=vcenter_hostname,
                vcenter_username=vcenter_username,
                vcenter_password=vcenter_password,
                agent_hostname=agent_hostname,
                agent_username=agent_username,
                agent_password=agent_password,
                metadata=metadata)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_volcoll(client_obj, volcoll_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
