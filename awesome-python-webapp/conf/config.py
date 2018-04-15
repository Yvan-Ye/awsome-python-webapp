#!/usr/bin/python
# -*- coding: UTF-8 -*-

#config.py

configs = config_default.configs

#用程序读取配置文件需要优先从config_override.py读取。为了简化读取配置文件，可以把所有配置读取到统一的config.py中
#merge用法以及作用
'''
int PyDict_Merge(PyObject *a, PyObject *b, int override)
Iterate over mapping object b adding key-value pairs to dictionary a. b may be a dictionary, or any object supporting PyMapping_Keys() and PyObject_GetItem(). If override is true, existing pairs in a will be replaced if a matching key is found in b, otherwise pairs will only be added if there is not a matching key in a. Return 0 on success or -1 if an exception was raised.
'''
try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass
    
