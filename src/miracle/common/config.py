# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
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

from oslo.config import cfg

from miracle.common import db
#from nova.openstack.common import rpc
#from nova import paths
#from nova import version

#import pbr.version

#version_info = pbr.version.VersionInfo('ccwsgi')
#version_string = version_info.version_string

def parse_args(argv, default_config_files=None):
    db.set_default_session()
#    rpc.set_defaults(control_exchange='nova')
    cfg.CONF(argv[1:],
             project='miracle',
             version='1.0',
             #version=version_string(),
             default_config_files=default_config_files)
    # init_db should behind cfg.CONF, because it user CONF.db_module_name to create db
    db.init_db()
