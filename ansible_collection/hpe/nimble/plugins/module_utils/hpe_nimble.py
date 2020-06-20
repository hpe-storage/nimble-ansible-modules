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

# this file will ultimately sit in "/usr/lib/python3.6/site-packages/ansible/module_ in production
import datetime
import uuid


def is_null_or_empty(name):
    if type(name) is bool:
        return False
    if name is None or not name or name == "":
        return True
    return False


def get_unique_string(baseName):
    unique_string = baseName + datetime.datetime.now().strftime(
        "-%d-%m-%Y") + '-' + str(uuid.uuid1().time)
    return unique_string


# remove arguments from kwargs which are by default none or empty
def remove_null_args(**kwargs):
    tosearch = kwargs.copy()
    for key, value in tosearch.items():
        if type(value) is not bool:
            if is_null_or_empty(value):
                kwargs.pop(key)
    return kwargs


def is_dict_same(server_dict, dict_to_check):
    if server_dict is None and dict_to_check is None:
        return True
    for key_to_check in dict_to_check.keys():
        # there can be two possibilities.
        # 1. key is not present. hence return false.
        # 2. key is present, but value is not same. return false for this too
        if key_to_check in server_dict.keys():
            if dict_to_check[key_to_check] == server_dict[key_to_check]:
                continue
            else:
                return False
        else:
            # key not present
            return False
    return True


def is_dict_item_present_on_server(server_list_of_dict, dict_to_check):

    if dict_to_check is None and server_list_of_dict is None:
        return True
    if type(server_list_of_dict) is not list:
        return False

    for server_dict in server_list_of_dict:
        if is_dict_same(server_dict, dict_to_check) is True:
            return True
    return False


# remove unchanged item from kwargs by matching them with the data present in given object attrs
def remove_unchanged_or_null_args(obj_attrs, **kwargs):
    params = remove_null_args(**kwargs)
    tosearch = params.copy()
    changed_attrs_dict = {}
    for key, value in tosearch.items():
        server_value = obj_attrs.attrs.get(key)

        if type(server_value) is list and type(value) is dict:
            # we will land here if the user wants to update a metadata.
            # server return a list of metadata dictionary
            temp_server_metadata_dict = {}
            for server_entry in server_value:
                temp_server_metadata_dict[server_entry['key']] = server_entry['value']
            if is_dict_same(temp_server_metadata_dict, value) is False:
                changed_attrs_dict[key] = value
                continue

        elif type(server_value) is dict and type(value) is dict:
            if is_dict_same(server_value, value) is False:
                changed_attrs_dict[key] = value
                continue

        elif type(server_value) is list and type(value) is list:
            # check if the list has dictionary to compare
            for entry_to_check in value:
                if type(entry_to_check) is dict:
                    if is_dict_item_present_on_server(server_value, entry_to_check) is True:
                        continue
                    else:
                        changed_attrs_dict[key] = value
                        # no need to further check for other keys as we already got one mismatch
                        break
                else:
                    server_value.sort()
                    value.sort()
                    if server_value != value:
                        changed_attrs_dict[key] = value
                        break

        elif server_value != value:
            # force is a special key used to force any operation for object
            # so that is never updated as an attribute
            if key != "force":
                changed_attrs_dict[key] = value
        else:
            # remove this from param from dictionary as value is same and already present on server
            params.pop(key)
    return (changed_attrs_dict, params)


def basic_auth_arg_fields():

    fields = {
        "hostname": {
            "required": True,
            "type": "str"
        },
        "username": {
            "required": True,
            "type": "str",
            "no_log": True
        },
        "password": {
            "required": True,
            "type": "str",
            "no_log": True
        }
    }
    return fields


def get_vol_id(client_obj, vol_name):
    if is_null_or_empty(vol_name):
        return None
    else:
        resp = client_obj.volumes.get(name=vol_name)
        if resp is None:
            raise Exception("Invalid value for volume: '%s'" % vol_name)
        return resp.attrs.get("id")


def get_volcoll_id(client_obj, volcoll_name):
    if is_null_or_empty(volcoll_name):
        return None
    else:
        resp = client_obj.volume_collections.get(name=volcoll_name)
        if resp is None:
            raise Exception("Invalid value for volcoll: '%s'" % volcoll_name)
        return resp.attrs.get("id")


def get_owned_by_group_id(client_obj, owned_by_group_name):
    if is_null_or_empty(owned_by_group_name):
        return None
    else:
        resp = client_obj.groups.get(name=owned_by_group_name)
        if resp is None:
            raise Exception("Invalid value for owned by group: '%s'" % owned_by_group_name)
        return resp.attrs.get("id")


def get_pool_id(client_obj, pool_name):
    if is_null_or_empty(pool_name):
        return None
    else:
        resp = client_obj.pools.get(name=pool_name)
        if resp is None:
            raise Exception("Invalid value for pool: '%s'" % pool_name)
        return resp.attrs.get("id")


def get_folder_id(client_obj, folder_name):
    if is_null_or_empty(folder_name):
        return None
    else:
        resp = client_obj.folders.get(name=folder_name)
        if resp is None:
            raise Exception("Invalid value for folder: '%s'" % folder_name)
        return resp.attrs.get("id")


def get_perfpolicy_id(client_obj, perfpolicy_name):
    if is_null_or_empty(perfpolicy_name):
        return None
    else:
        resp = client_obj.performance_policies.get(name=perfpolicy_name)
        if resp is None:
            raise Exception("Invalid value for performance policy: '%s'" % perfpolicy_name)
        return resp.attrs.get("id")


def get_prottmpl_id(client_obj, prottmpl_name):
    if is_null_or_empty(prottmpl_name):
        return None
    else:
        resp = client_obj.protection_templates.get(name=prottmpl_name)
        if resp is None:
            raise Exception("Invalid value for protection template: '%s'" % prottmpl_name)
        return resp.attrs.get("id")


def get_chap_user_id(client_obj, chap_user_name):
    if is_null_or_empty(chap_user_name):
        return None
    else:
        resp = client_obj.chap_users.get(name=chap_user_name)
        if resp is None:
            raise Exception("Invalid value for chap user: '%s'" % chap_user_name)
        return resp.attrs.get("id")


def get_pe_id(client_obj, pe_name):
    if is_null_or_empty(pe_name):
        return None
    else:
        resp = client_obj.protocol_endpoints.get(name=pe_name)
        if resp is None:
            raise Exception("Invalid value for protection endpoint: '%s'" % pe_name)
        return resp.attrs.get("id")


def get_snapshot_id(client_obj, snap_name):
    if is_null_or_empty(snap_name):
        return None
    else:
        resp = client_obj.snapshots.get(name=snap_name)
        if resp is None:
            raise Exception("Invalid value for snapshot: '%s'" % snap_name)
        return resp.attrs.get("id")


def get_replication_partner_id(client_obj, replication_partner_name):
    if is_null_or_empty(replication_partner_name):
        return None
    else:
        resp = client_obj.replication_partners.get(name=replication_partner_name)
        if resp is None:
            raise Exception("Invalid value for replication partner: '%s'" % replication_partner_name)
        return resp.attrs.get("id")


def get_volcoll_or_prottmpl_id(client_obj, volcoll_name, prot_template_name):
    if is_null_or_empty(volcoll_name) and is_null_or_empty(prot_template_name):
        return None
    if is_null_or_empty(volcoll_name) is False and is_null_or_empty(prot_template_name) is False:
        raise Exception("Volcoll and prot_template are mutually exlusive. Please provide either one of them.")
    else:
        if volcoll_name is not None:
            resp = get_volcoll_id(client_obj, volcoll_name)
            if resp is None:
                raise Exception("Invalid value for volcoll: '%s'" % volcoll_name)
        elif prot_template_name is not None:
            resp = get_prottmpl_id(client_obj, prot_template_name)
            if resp is None:
                raise Exception("Invalid value for protection template: '%s'" % prot_template_name)
        return resp


def get_downstream_partner_id(client_obj, downstream_partner):
    if is_null_or_empty(downstream_partner):
        return None
    else:
        resp = client_obj.replication_partners.get(name=downstream_partner)
        if resp is None:
            raise Exception("Invalid value for downstream partner: '%s'" % downstream_partner)
        return resp.attrs.get("id")
