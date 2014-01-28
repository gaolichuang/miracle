# -*- coding: UTF-8 -*-
'''
Created on 2014.1.1

@author: gaolichuang
'''

import sys

from oslo.config import cfg

from miracle.common import config
from miracle.common.base import log as logging
from miracle.tests.common.db import api as db_api
from miracle.common.utils import timeutils
from miracle.common.db.sqlalchemy import session
from miracle.common.db import utils

    

def main():
    config.parse_args(sys.argv)
    logging.setup("miracle")

    print 'insert many data without orm'
    db_api.user_insert_many_data()

    print 'get all'
    ret = db_api.user_get_all()
    print ret

    values = {'id':17}
    print 'get value id %s'% values['id']
    db_api.user_get_filter_dict(values)

    db_api.user_get_filter_bynum()
    
    values = {'name':'alexa',
              'name1':'我们',
              'sex':'man',
              'age':20,
              'created_at':timeutils.utcnow()}
#    db_api.user_insert(values)
#    db_api.user_insert1(values)
#    db_api.user_insert2(values)    


    values = {'id':21,'name':'YYYYYYY',
              'name1':'我们',
              'sex':'man',
              'age':20,
              'created_at':timeutils.utcnow()}
#db_api.user_update1(values)
    db_api.user_update2(values)

    values = {'id':11}
    db_api.user_get_filter_delete1(values)

    values = {'id':12}
    db_api.user_get_filter_delete(values)

    values = {'id':20}
    db_api.user_soft_del(values)

if __name__ == '__main__':
    main()

