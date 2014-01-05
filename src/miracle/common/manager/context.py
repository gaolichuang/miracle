# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
TODO: now context only have uuid, you can add globale info in futrue
"""

from miracle.common.utils import uuidutils

def generate_id():
    return 'manager-%s' % uuidutils.generate_uuid()

class ManagerContext(object):

    """Helper class to represent useful information about a manager context.

    Stores information about the security context under which the user
    accesses the system, as well as additional request information.
    """

    def __init__(self, m_id=None):

        if not m_id:
            m_id = generate_id()
        self.m_id = m_id

    def to_dict(self):
        return {'m_id': self.m_id}
    @property
    def manager_id(self):
        return self.m_id

def get_manager_context(show_deleted=False):
    context = ManagerContext(None)
    return context
