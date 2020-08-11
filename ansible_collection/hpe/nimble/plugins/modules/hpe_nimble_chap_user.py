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
description: Manage CHAP user on HPE Nimble Storage group.
module: hpe_nimble_chap_user
options:
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing CHAP user.
  description:
    required: False
    type: str
    description:
    - Text description of CHAP user.
  initiator_iqns:
    required: False
    type: list
    description:
    - List of iSCSI initiators. To be configured with this CHAP user for iSCSI Group Target CHAP authentication. This attribute
      cannot be modified at the same time with other attributes. If any specified initiator is already associated with another CHAP
      user, it will be replaced by this CHAP user for future CHAP authentication.
  name:
    required: True
    type: str
    description:
    - Name of CHAP user.
  password:
    required: False
    type: str
    description:
    - CHAP secret. The CHAP secret should be between 12-16 characters and cannot contain spaces or most punctuation.
      string of 12 to 16 printable ASCII characters excluding ampersand and ^[];`
  state:
    required: True
    choices:
    -  create
    -  present
    -  absent
    type: str
    description:
    - Choice for chap user operation.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage CHAP user.
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create, then create chap user, fails if it exist or cannot create
# if state is present, then create chap user if not present, else success
- name: Create Chap User
  hpe_nimble_chap_user:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    description: "{{ description }}"
    user_password: "{{ user_password | mandatory }}"
    state: "{{ state | default('present') }}"

- name: Delete Chap User
  hpe_nimble_chap_user:
    host: "{{ host }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    state: "absent"

'''
RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from nimbleclient.v1 import client
except ImportError:
    client = None
import ansible_collections.hpe.nimble.plugins.module_utils.hpe_nimble as utils


def create_chap_user(
        client_obj,
        user_name,
        password,
        **kwargs):

    if utils.is_null_or_empty(user_name):
        return (False, False, "Create chap user failed as user is not present.", {})
    if utils.is_null_or_empty(password):
        return (False, False, "Create chap user failed as password is not present.", {})

    try:
        user_resp = client_obj.chap_users.get(id=None, name=user_name)
        if utils.is_null_or_empty(user_resp):
            params = utils.remove_null_args(**kwargs)
            user_resp = client_obj.chap_users.create(name=user_name, password=password, **params)
            return (True, True, f"Chap user '{user_name}' created successfully.", {})
        else:
            return (False, False, f"Chap user '{user_name}' cannot be created as it is already present.", {})
    except Exception as ex:
        return (False, False, f"Chap user creation failed |{ex}", {})


def update_chap_user(
        client_obj,
        user_name,
        user_password,
        **kwargs):

    if utils.is_null_or_empty(user_name):
        return (False, False, "Update chap user failed as user is not present.", {})

    try:
        user_resp = client_obj.chap_users.get(id=None, name=user_name)
        if utils.is_null_or_empty(user_resp):
            return (False, False, f"Chap user '{user_name}' cannot be updated as it is not present.", {})

        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(user_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            user_resp = client_obj.chap_users.update(id=user_resp.attrs.get("id"), password=user_password, **params)
            return (True, True, f"Chap user '{user_name}' already present. Modified the following fields :", changed_attrs_dict)
        else:
            return (True, False, f"Chap user '{user_resp.attrs.get('name')}' already present.", {})
    except Exception as ex:
        return (False, False, f"Chap user update failed |{ex}", {})


def delete_chap_user(
        client_obj,
        user_name):

    if utils.is_null_or_empty(user_name):
        return (False, False, "Delete chap user failed as user is not present.", {})

    try:
        user_resp = client_obj.chap_users.get(id=None, name=user_name)
        if utils.is_null_or_empty(user_resp):
            return (False, False, f"Chap user '{user_name}' cannot be deleted as it is not present.", {})

        client_obj.chap_users.delete(id=user_resp.attrs.get("id"))
        return (True, True, f"Deleted chap user '{user_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Delete chap user failed |{ex}", {})


def main():

    fields = {
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
        "initiator_iqns": {
            "required": False,
            "type": "list",
            "no_log": False
        },
        "name": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "user_password": {
            "required": False,
            "type": "str",
            "no_log": True
        },
        "state": {
            "required": True,
            "choices": ['create',
                        'present',
                        'absent'
                        ],
            "type": "str"
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    required_if = [('state', 'create', ['user_password'])]

    module = AnsibleModule(argument_spec=fields, required_if=required_if)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    change_name = module.params["change_name"]
    description = module.params["description"]
    initiator_iqns = module.params["initiator_iqns"]
    user_name = module.params["name"]
    user_password = module.params["user_password"]
    state = module.params["state"]

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
        if not client_obj.chap_users.get(id=None, name=user_name) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_chap_user(
                client_obj,
                user_name,
                user_password,
                description=description)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_chap_user(
                client_obj,
                user_name,
                user_password,
                name=change_name,
                description=description,
                initiator_iqns=initiator_iqns)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_chap_user(client_obj, user_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
