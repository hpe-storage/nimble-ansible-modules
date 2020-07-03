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
description: Manage shelves on HPE Nimble Storage group.
module: hpe_nimble_shelf
options:
  accept_dedupe_impact:
    required: False
    type: bool
    description:
    - Accept the reduction or elimination of deduplication capability on the system as a result of activating a shelf
      that does not meet the necessary deduplication requirements.
  accept_foreign:
    required: False
    type: bool
    description:
    - Accept the removal of data on the shelf disks and activate foreign shelf.
  activated:
    required: True
    type: bool
    description:
    - Activated state for shelf or disk set means it is available to store date on. An activated shelf may not be deactivated.
  driveset:
    required: False
    type: int
    description:
    - Driveset to activate.
  force:
    required: False
    type: bool
    description:
    - Forcibly activate shelf.
  last_request:
    required: False
    type: bool
    description:
    - Indicates this is the last request in a series of shelf add requests.
  state:
    required: True
    choices:
    - present
    type: str
    description:
    - Choice for shelf operation.
  shelf_serial:
    required: True
    type: str
    description:
    - Serial number of shelf.
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage shelves.
version_added: 2.9
'''

EXAMPLES = r'''

- name: Update shelf
  hpe_nimble_shelf:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    shelf_serial: "{{ shelf_serial | mandatory }}"
    accept_foreign: "{{ accept_foreign }}"
    force: "{{ force }}"
    activated: "{{ activated }}"
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

def update_shelve(
        client_obj,
        shelf_serial,
        **kwargs):

    if utils.is_null_or_empty(shelf_serial):
        return (False, False, "Shelf update failed as no shelf id provided.")

    try:
        shelf_resp = client_obj.shelves.get()
        if utils.is_null_or_empty(shelf_resp):
            return (False, False, f"Shelf serial '{shelf_serial}' is not present on array.")
        else:
            # check if the given shelf serial is present on array
            if shelf_serial == shelf_resp.attrs.get("serial"):
                changed_attrs_dict, params = utils.remove_unchanged_or_null_args(shelf_resp, **kwargs)
                if changed_attrs_dict.__len__() > 0:
                    shelf_resp = client_obj.shelves.update(id=shelf_resp.attrs.get("id"), **params)
                    return (True, True, f"Successfully updated Shelf '{shelf_serial}'.")
                else:
                    return (True, False, f"Shelf serial '{shelf_serial}' already updated.", {})
            else:
                return (False, False, f"Shelf serial '{shelf_serial}' not found.")
    except Exception as e:
        return (False, False, "Shelf update failed | %s" % str(e))


def main():

    fields = {
        "state": {
            "required": True,
            "choices": ['present'],
            "type": "str"
        },
        "shelf_serial": {
            "required": True,
            "type": "str",
            "no_log": False
        },
        "activated": {
            "required": True,
            "type": "bool",
            "no_log": False
        },
        "driveset": {
            "required": False,
            "type": "int",
            "no_log": False
        },
        "force": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "accept_foreign": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "accept_dedupe_impact": {
            "required": False,
            "type": "bool",
            "no_log": False
        },
        "last_request": {
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

    hostname = module.params["hostname"]
    username = module.params["username"]
    password = module.params["password"]
    state = module.params["state"]
    shelf_serial = module.params["shelf_serial"]
    activated = module.params["activated"]
    driveset = module.params["driveset"]
    force = module.params["force"]
    accept_foreign = module.params["accept_foreign"]
    accept_dedupe_impact = module.params["accept_dedupe_impact"]
    last_request = module.params["last_request"]

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
        return_status, changed, msg = update_shelve(
            client_obj,
            shelf_serial,
            activated=activated,
            driveset=driveset,
            force=force,
            accept_foreign=accept_foreign,
            accept_dedupe_impact=accept_dedupe_impact,
            last_request=last_request)

    if return_status:
        module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()
