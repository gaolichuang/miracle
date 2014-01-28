# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Implementation of SQLAlchemy backend.

Created on 2013.12.30

@author: gaolichuang@gmail.com
"""

from random import randint

from oslo.config import cfg

from miracle.tests.common.db import models
from miracle.common.db.sqlalchemy import session as db_session
from miracle.common.db import utils



def user_insert_many_data():
    '''not use orm may get more efficiency inreturn'''
    session = db_session.get_session()
    with session.begin():
        session.execute(
                models.User.__table__.insert(),
                [{'name': `randint(1, 100)`,'age': randint(1, 100)} for i in xrange(100)]
                )
def user_get_all():
    session = db_session.get_session()
    ret = session.query(models.User).all()
    return ret

def user_get_filter_dict(filter_dict):
    sa = db_session.get_session()
    users =  sa.query(models.User).filter_by(**filter_dict).all()

    for user in users:
        print '='*80
        for key,value in user.iteritems():
            print key, value


def user_get_filter_bynum(num = 20):
    '''query specific number row'''
    session = db_session.get_session()
# status_ref.update(values)
    with session.begin():
        ret = session.query(models.User).filter(models.User.id > 100, models.User.id < num).limit(20).all()
        for r in ret:
            print r.id
        return ret

def user_insert(values):
    utils.convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
    status_ref = models.User()
    for (key, value) in values.iteritems():
        status_ref[key] = value
    status_ref.save()
    return status_ref
def user_insert1(values):
    utils.convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
    status_ref = models.User()
    status_ref.update(values)
    status_ref.save()
    return status_ref
def user_insert2(values):
    utils.convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
    session = db_session.get_session()
    status_ref = models.User()
    status_ref.update(values)
    with session.begin():
        session.add(status_ref)

def user_update1(values):
    utils.convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
    session = db_session.get_session()
    status_ref = models.User()
    status_ref.update(values)
    with session.begin():
        session.merge(status_ref)
def user_update2(values):
    utils.convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
    status_ref = models.User()
    for (key, value) in values.iteritems():
        status_ref[key] = value
    status_ref.save(update = True)
    return status_ref

def user_get_filter_delete(filter_dict):
## filter_by usage
    '''filter you can refere nova.db.api.flavor_get_all'''
    sa = db_session.get_session()
    sa.query(models.User).filter_by(**filter_dict).delete()

def user_get_filter_delete1(filter_dict):
    sa = db_session.get_session()
    for ins in  sa.query(models.User).filter_by(**filter_dict):
        sa.delete(ins)
        sa.flush()

def user_soft_del(values):
    status_ref = models.User()
    for (key, value) in values.iteritems():
        status_ref[key] = value
    status_ref.soft_delete()
    return status_ref

