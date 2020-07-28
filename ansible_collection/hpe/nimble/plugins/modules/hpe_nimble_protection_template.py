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
description: Manage protection templates on HPE Nimble Storage group.
module: hpe_nimble_protection_template
options:
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
    - If the application is running within a windows cluster environment, this is the cluster name.
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
  app_service_name:
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
    default: none
    description:
    - Application synchronization.
  change_name:
    required: False
    type: str
    description:
    - Change name of the existing protection template.
  description:
    required: False
    type: str
    description:
    - Text description of protection template.
  name:
    required: True
    type: str
    
    description:
    - Name of protection template.
  state:
    required: True
    choices:
        - present
        - absent
        - create
    type: str
    description:
    - Choice for protection template operations.
  vcenter_hostname:
    required: False
    type: str
    description:
    - VMware vCenter hostname.
  vcenter_password:
    required: False
    type: str
    description:
    - Application VMware vCenter password. A password with few constraints.
  vcenter_username:
    required: False
    type: str
    description:
    - Application VMware vCenter username. String of up to 80 alphanumeric characters, beginning with a letter.
      It can include ampersand (@), backslash (\), dash (-), period (.), and underscore (_).
extends_documentation_fragment: hpe_nimble
short_description: Manage HPE Nimble Storage protection templates.
version_added: 2.9
'''

EXAMPLES = r'''

# if state is create , then create a protection template if not present. Fails if already present.
# if state is present, then create a protection template if not present. Succeed if it already exists.
- name: Create protection template if not present
  hpe_nimble_protection_template:
    hostname: "{{ hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    name: "{{ name }}"
    description: "{{ description | default(None)}}"
    state: "{{ state | default('present') }}"

- name: Delete protection template
  hpe_nimble_protection_template:
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

def create_prot_template(
        client_obj,
        prot_template_name,
        **kwargs):

    if utils.is_null_or_empty(prot_template_name):
        return (False, False, "Create protection template failed as protection template name is not present.", {})
    try:
        prot_template_resp = client_obj.protection_templates.get(id=None, name=prot_template_name)
        if utils.is_null_or_empty(prot_template_resp):
            params = utils.remove_null_args(**kwargs)
            prot_template_resp = client_obj.protection_templates.create(name=prot_template_name, **params)
            return (True, True, f"Protection template '{prot_template_name}' created successfully.", {})
        else:
            return (False, False, f"Protection template '{prot_template_name}' cannot be created as it is already present.", {})
    except Exception as ex:
        return (False, False, f"Protection template creation failed | {ex}", {})


def update_prot_template(
        client_obj,
        prot_template_resp,
        **kwargs):

    if utils.is_null_or_empty(prot_template_resp):
        return (False, False, "Update protection template failed as protection template is not present.", {})
    try:
        prot_template_name = prot_template_resp.attrs.get("name")
        changed_attrs_dict, params = utils.remove_unchanged_or_null_args(prot_template_resp, **kwargs)
        if changed_attrs_dict.__len__() > 0:
            prot_template_resp = client_obj.protection_templates.update(id=prot_template_resp.attrs.get("id"), **params)
            return (True, True, f"Protection template '{prot_template_name}' already Present. Modified the following fields :", changed_attrs_dict)
        else:
            return (True, False, f"Protection template '{prot_template_name}' already present.", {})
    except Exception as ex:
        return (False, False, f"Protection template update failed | {ex}", {})


def delete_prot_template(client_obj, prot_template_name):

    if utils.is_null_or_empty(prot_template_name):
        return (False, False, "Protection template deletion failed as protection template name is not present.", {})

    try:
        prot_template_resp = client_obj.protection_templates.get(id=None, name=prot_template_name)
        if utils.is_null_or_empty(prot_template_resp):
            return (False, False, f"Protection template '{prot_template_name}' not present to delete.", {})
        else:
            client_obj.protection_templates.delete(id=prot_template_resp.attrs.get("id"))
            return (True, True, f"Deleted protection template '{prot_template_name}' successfully.", {})
    except Exception as ex:
        return (False, False, f"Protection template deletion failed | {ex}", {})


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
        "app_service_name": {
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
    prot_template_name = module.params["name"]
    change_name = module.params["change_name"]
    description = module.params["description"]
    app_sync = module.params["app_sync"]
    app_server = module.params["app_server"]
    app_id = module.params["app_id"]
    app_cluster = module.params["app_cluster"]
    app_service_name = module.params["app_service_name"]
    vcenter_hostname = module.params["vcenter_hostname"]
    vcenter_username = module.params["vcenter_username"]
    vcenter_password = module.params["vcenter_password"]
    agent_hostname = module.params["agent_hostname"]
    agent_username = module.params["agent_username"]
    agent_password = module.params["agent_password"]

    if (username is None or password is None or hostname is None or prot_template_name is None):
        module.fail_json(
            msg="Missing variables: hostname, username, password and protection template is mandatory.")

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
        prot_template_resp = client_obj.protection_templates.get(id=None, name=prot_template_name)
        if utils.is_null_or_empty(prot_template_resp) or state == "create":
            return_status, changed, msg, changed_attrs_dict = create_prot_template(
                client_obj,
                prot_template_name,
                description=description,
                app_sync=app_sync,
                app_server=app_server,
                app_id=app_id,
                app_cluster_name=app_cluster,
                app_service_name=app_service_name,
                vcenter_hostname=vcenter_hostname,
                vcenter_username=vcenter_username,
                vcenter_password=vcenter_password,
                agent_hostname=agent_hostname,
                agent_username=agent_username,
                agent_password=agent_password)
        else:
            # update op
            return_status, changed, msg, changed_attrs_dict = update_prot_template(
                client_obj,
                prot_template_resp,
                name=change_name,
                description=description,
                app_sync=app_sync,
                app_server=app_server,
                app_id=app_id, app_cluster_name=app_cluster,
                app_service_name=app_service_name,
                vcenter_hostname=vcenter_hostname,
                vcenter_username=vcenter_username,
                vcenter_password=vcenter_password,
                agent_hostname=agent_hostname,
                agent_username=agent_username,
                agent_password=agent_password)

    elif state == "absent":
        return_status, changed, msg, changed_attrs_dict = delete_prot_template(client_obj, prot_template_name)

    if return_status:
        if changed_attrs_dict:
            module.exit_json(return_status=return_status, changed=changed, message=msg, modified_attrs=changed_attrs_dict)
        else:
            module.exit_json(return_status=return_status, changed=changed, msg=msg)
    else:
        module.fail_json(return_status=return_status, changed=changed, msg=msg)


if __name__ == '__main__':
    main()