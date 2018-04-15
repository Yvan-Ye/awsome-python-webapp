#!/usr/bin/python
# -*- coding: UTF-8 -*-

#config_override.py 作为生产环境的标准配置

#如果要部署到服务器时，通常需要修改数据库的host等信息
config = {
    'db': {
        'host': '192.168.0.100'
    }
}