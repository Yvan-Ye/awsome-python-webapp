#!/usr/bin/python
# -*- coding: UTF-8 -*-

#user.py


from orm import Model, StringField, IntegerField
#创建user对象 与数据库users关联
class User(Model):
    __table__ = 'users'
    
    id = IntegerField(primary_key=True)
    name = StringField()
    

#create instance:
user = User(id=123, name = 'Yvan')
#save in database:
user.insert()
#inquire all User object :
users = User.findAll()