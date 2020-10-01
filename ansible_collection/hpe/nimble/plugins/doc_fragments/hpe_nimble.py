#!/usr/bin/env python

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


class ModuleDocFragment(object):

    # HPE Nimble doc fragment
    DOCUMENTATION = '''
options:
  host:
    description:
    - HPE Nimble Storage IP address.
    required: True
    type: str
  password:
    description:
    - HPE Nimble Storage password.
    required: True
    type: str
  username:
    description:
    - HPE Nimble Storage user name.
    required: True
    type: str
requirements:
  - Ansible 2.9 or later
  - Python 3.6 or later
  - HPE Nimble Storage SDK for Python
  - HPE Nimble Storage arrays running NimbleOS 5.0 or later

notes:
  -  check_mode is not supported.
'''
