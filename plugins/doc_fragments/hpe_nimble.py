# Copyright: (c) 2020, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+
# author alok ranjan (alok.ranjan2@hpe.com)


class ModuleDocFragment(object):

    # HPE Nimble doc fragment
    DOCUMENTATION = '''
options:
    hostname:
        description:
        - "The storage system IP address."
        required: True
        type: str
    password:
        description:
        - "The storage system password."
        required: True
        type: str
    username:
        description:
        - "The storage system user name."
        required: True
        type: str

requirements:
  - "Nimble OS 5.1.x"
  - "Ansible - 2.9"
  - nimble-sdk >= 1.0.1. Install using 'pip install nimble-sdk'
  - "REST service should be enabled on the Nimble storage array."

notes:
  -  check_mode not supported
    '''
