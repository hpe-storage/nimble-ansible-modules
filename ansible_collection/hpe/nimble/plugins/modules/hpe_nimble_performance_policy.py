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
description:  Manage performance policies on HPE Nimble Storage group.
module: hpe_nimble_performance_policy
options:
  app_category:
    required: False
    type: str
    description:
    - Specifies the application category of the associated volume.
  block_size:
    required: False
    type: int
    description:
    - Block Size in bytes to be used by the volumes created with this specific performance policy. Supported block sizes are
      4096 bytes (4 KB), 8192 bytes (8 KB), 16384 bytes(16 KB), and 32768 bytes (32 KB). Block size of a performance policy cannot
      be changed once the performance policy is created.
  cache:
    required: False
    type: bool
    default: True
    description:
    - Flag denoting if data in the associated volume should be cached.
  cache_policy:
    required: False
    choices:
    - disabled
    - normal
    - aggressive
    - no_write
    - aggressive_read_no_write
    type: str
    description:
    - Specifies how data of associated volume should be cached. Normal policy caches data but skips in certain conditions such as
      sequential I/O. Aggressive policy will accelerate caching of all data belonging to this volume, regardless of sequentiality.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing performance policy.
  compress:
    required: False
    type: bool
    default: True
    description:
    - Flag denoting if data in the associated volume should be compressed.
  description:
    required: False
    type: str
    description:
    - Description of a performance policy.
  dedupe:
    required: False
    type: bool
    default: False
    description:
    - Specifies if dedupe is enabled for volumes created with this performance policy.
  name:
    required: True
    type: str
    description:
    - Name of the performance policy.
  space_policy:
    required: False
    choices:
    - invalid
    - offline
    - non_writable
    - read_only
    - login_only
    type: str
    description:
    - Specifies the state of the volume upon space constraint violation such as volume limit violation or volumes above their volume reserve,
      if the pool free space is exhausted. Supports two policies, 'offline' and 'non_writable'.
  state:
    required: True
    choices:
    - present
    - absent
    - create
    type: str
    description:
    - Choice for performance policy operation.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage performance policies
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create , then create a performance policy if not present. Fails if already present.
# if state is present, then create a performance policy if not present. Succeed if it already exists.
- name: Create performance policy if not present
  hpe_nimble_performance_policy:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: "{{ state | default('present') }}"
    name: "{{ name }}"
    description: "{{ description }}"
    block_size: "{{ block_size }}"
    compress: "{{ compress }}"

- name: Delete performance policy
  hpe_nimble_performance_policy:
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

def create_perf_policy(
        client_obj,
        perf_policy_name,
        **kwargs):

    if utils.is_null_or_empty(perf_policy_name):
        return (False, False, "Create performance policy failed. Performance policy name is not present.", {})

    try:
        perf_policy_resp = client_obj.performance_policies.get(id=None, name=perf_policy_name)
        if utils.is_null_or_empty(perf_policy_resp):
            params = utils.remove_null_args(**kwargs)
            perf_policy_resp = client_obj.performance_policies.create(name=perf_policy_name,
                                                                      **params)
            if perf_policy_resp is not None:
                return (True, True, f"Created performance policy '{perf_policy_name}' successfully.", {})
        else:
            return (False, False, f"Cannot create Performance policy '{perf_policy_name}' as it is already present", {})
    except Exception as ex:
        return (False, False, f"Performance policy creation failed | {ex}", {})


def update_perf_policy(
        client_obj,
        perf_policy_resp,
        **kwargs):

    if utils.is_null_or_empty(perf_policy_resp):
        return (False, False, "Update performance policy failed. Performance policy name is not present.", {})

    try:
        perf_policy_name = perf_policy_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(perf_policy_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            perf_policy_resp = client_obj.performance_policies.update(id=perf_policy_resp.attrs.get("id"), **params)
            return (True, True, f"Performance policy '{perf_policy_name}' already present. Modified the following fields:", changed_attrs_dict)
        else:
            return (True, False, f"Performance policy '{perf_policy_name}' already present.", {})
    except Exception as ex:
        return (False, False, f"Performance policy update failed | {ex}", {})


def delete_perf_policy(
        client_obj,
        perf_policy_name):

    if utils.is_null_or_empty(perf_policy_name):
        return (False, False, "Delete performance policy failed. Performance policy name is not present.", {})

    try:
        perf_policy_resp = client_obj.performance_policies.get(id=None, name=perf_policy_name)
        if utils.is_null_or_empty(perf_policy_resp):
            return (False, False, f"Cannot delete Performance policy '{perf_policy_name}' as it is not present ", {})
        else:
            perf_policy_resp = client_obj.performance_policies.delete(id=perf_policy_resp.attrs.get("id"))
            return (True, True, f"Deleted performance policy '{perf_policy_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Performance policy deletion failed | {ex}", {})


def main():

    fields = {
        "app_category": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "block_size": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "cache": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "cache_policy": {
            "required": False,
            "choices": ['disabled', 'normal', 'aggressive', 'no_write', 'aggressive_read_no_write'],
            "type": "str",
            "no_log": False
        },
        "change_name": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "compress": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "description": {
            "required": False,
            "type": "str",
            "no_log": False
        },
        "dedupe": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "name": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "space_policy": {
            "required": False,
            "choices": ['invalid', 'offline', 'non_writable', 'read_only', 'login_only'],
            "type": "str",
            "no_log": False
        },
        "state": {
            "required": True,
            "choices": ['present',
                        'absent',
                        'create'
                        ],
            "type": "str"
        }
    }
    default_fields = utils.basic_auth_arg_fields()
    fields.update(default_fields)
    module = AnsibleModule(argument_spec=fields)
    if client is None:
        module.fail_json(msg='Python nimble-sdk could not be found.')

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    app_category = module.params["app_category"]
    block_size = module.params["block_size"]
    cache = module.params["cache"]
    cache_policy = module.params["cache_policy"]
    compress = module.params["compress"]
    description = module.params["description"]
    dedupe = module.params["dedupe"]
    perf_policy_name = module.params["name"]
    change_name = module.params["change_name"]
    space_policy = module.params["space_policy"]
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
        perf_policy_resp = client_obj.performance_policies.get(id=None, name=perf_policy_name)
        if utils.is_null_or_empty(perf_policy_resp) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_perf_policy(
                client_obj,
                perf_policy_name,
                app_category=app_category,
                block_size=block_size,
                cache=cache,
                cache_policy=cache_policy,
                compress=compress,
                description=description,
                dedupe_enabled=dedupe,
                space_policy=space_policy)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_perf_policy(
                client_obj,
                perf_policy_resp,
                name=change_name,
                app_category=app_category,
                cache=cache,
                cache_policy=cache_policy,
                compress=compress,
                description=description,
                dedupe_enabled=dedupe,
                space_policy=space_policy)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_perf_policy(
            client_obj,
            perf_policy_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
