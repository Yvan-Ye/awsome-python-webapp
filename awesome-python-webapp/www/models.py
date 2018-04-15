


import time,uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)
    
class User(Model):
    __table__ = 'users'
    
    id = StringField(primary_key =True, default = next_id, ddl='varchar(50)')
    email = StringField (ddl = 'varchar(50)')
    passwd =StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default = time.time)
    
class Blog(Model):
    __table__='blog'
    
    id = StringField(primary_key=True, default = next_id, ddl='varchar(50)')
    user_id=StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = 
    
    
    
    
    
'''
如果你不想字段为 NULL 可以设置字段的属性为 NOT NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
AUTO_INCREMENT定义列为自增的属性，一般用于主键，数值会自动加1。
PRIMARY KEY关键字用于定义列为主键。 您可以使用多列来定义主键，列间以逗号分隔。
ENGINE 设置存储引擎，CHARSET 设置编码。

'''