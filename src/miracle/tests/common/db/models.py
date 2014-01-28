# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
SQLAlchemy models Sample.

Created on 2013.12.30

@author: gaolichuang@gmail.com
http://www.keakon.net/2012/12/03/SQLAlchemy%E4%BD%BF%E7%94%A8%E7%BB%8F%E9%AA%8C

CREATE TABLE user (
        updated_at DATETIME, 
        deleted_at DATETIME, 
        deleted INTEGER, 
        id INTEGER NOT NULL, 
        name VARCHAR(255), 
        sex VARCHAR(20), 
        age INTEGER, 
        schoolid INTEGER, 
        created_at DATETIME, 
        PRIMARY KEY (id), 
        FOREIGN KEY(schoolid) REFERENCES school (id)
);
"""

from sqlalchemy import Column, Index, Integer, BigInteger, Enum, String, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, Float
#from sqlalchemy.orm import relationship, backref, object_mapper

from miracle.common.db.sqlalchemy import models

# this must be here!!! use this to create tables
BASE = declarative_base()

'''
create table
Above, the declarative_base() callable returns a new base class from
 which all mapped classes should inherit. When the class definition
 is completed, a new Table and mapper() will have been generated.
 http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
'''
class User(BASE, models.MixinModelBase):
    __tablename__ = 'user'
    __table_args__ = ()
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    name1 = Column('name1', Text)
    sex = Column('sex',String(20))
    age = Column('age',Integer)
    school_id = Column('schoolid', Integer, ForeignKey('school.id'))
    created_at = Column('created_at',DateTime)

class School(BASE):
    __tablename__ = 'school'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))  # 
