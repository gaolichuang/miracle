"""
Implementation of SQLAlchemy backend.

Created on 2014.1.27

@author: gaolichuang@gmail.com
"""

import collections
import copy
import datetime
import functools
import itertools
import sys
import time
import uuid

from oslo.config import cfg

from miracle.common.db.sqlalchemy import session as db_session
from miracle.common.utils import importutils

db_default_opts = [
    cfg.StrOpt('default_sqlitedb_name',
               default='sqlite_default.db',
               help='default sqlite default name'),
    cfg.StrOpt('db_module_name',
               default='',
               help='project use module name, make sure you assign it')
]
#rpc = importutils.try_import('nova.openstack.common.rpc')
CONF = cfg.CONF
CONF.register_opts(db_default_opts)

_DEFAULT_SQL_CONNECTION = 'sqlite:///' + CONF.default_sqlitedb_name

def set_default_session():
    db_session.set_defaults(sql_connection=_DEFAULT_SQL_CONNECTION,
                            sqlite_db='nova.sqlite')
def init_db():
    '''create table, make suer you assign the right model'''
    if not CONF.db_module_name == '':
        engine = db_session.get_engine()
        models = importutils.import_module(CONF.db_module_name)
        models.BASE.metadata.create_all(engine)
