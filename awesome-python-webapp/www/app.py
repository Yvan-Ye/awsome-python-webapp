#下面这句是表示在liunx下的路径，用以执行Python 环境变量？
#!/usr/bin/env python3
#下面这句是表示该文件是用utf-8编码的形式进行编码的
# -*- coding: utf-8 -*-
#app.py
#CREATE date: 2108-1-26
#update date: 2018-2-28

#定义变量__author__，通常用来表示这段代码的作者
__author__ = 'Yvan Ye'

'''
async web application.
'''

#导入外部函数，在本文中使用
#logging函数是用于Python内置的logging模块可以非常容易地记录错误信息。通过配置，logging还可以把错误记录到日志文件里，方便事后排查。 logging.info()就可以输出一段文本。这就是logging的好处，它允许你指定记录信息的级别，有debug，info，warning，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了。同理，指定level=WARNING后，debug和info就不起作用了。这样一来，你可以放心地输出不同级别的信息，也不用删除，最后统一控制输出哪个级别的信息。后面那个config那段是不可或缺的
import logging; logging.basicConfig(level=logging.INFO)
#asyncio 外部模块是asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。
#os外部模块是其实操作系统提供的命令只是简单地调用了操作系统提供的接口函数，Python内置的os模块也可以直接调用操作系统提供的接口函数。
#json外部模块是IO 序列化的内容
'''
如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便。

JSON表示的对象就是标准的JavaScript语言的对象，JSON和Python内置的数据类型对应如下
'''
#time外部模块是http://www.jb51.net/article/75364.htm

import asyncio, os, json, time
#datetime外面模块是Python处理日期和时间的标准库。 注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类。
from datetime import datetime
#从aiohttp内导入web这个函数,
'''
如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。
asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。
'''
from aiohttp import web
#index函数，接收request参数，返回一个web body
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')
'''
用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

把@asyncio.coroutine替换为async；
把yield from替换为await。
'''
#协程函数 init
async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
#创建一个事件循环
loop.run_until_complete(init(loop))
'''
Run until the init(loop) is done.
将协程注册到事件循环，并启动事件循环
If the argument is a coroutine object, it is wrapped by ensure_future().

Return the Future’s result, or raise its exception.
'''
loop.run_forever()
'''
Run until stop() is called. 
'''