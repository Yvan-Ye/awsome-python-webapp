#下面这句是表示在liunx下的路径，用以执行Python 环境变量？
#!/usr/bin/env python3
#下面这句是表示该文件是用utf-8编码的形式进行编码的
# -*- coding: utf-8 -*-
#app.py
#CREATE date: 2108-1-26
#update date: 2018-4-13

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
#json外部模块是 IO 序列化的内容
'''
如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便。

JSON表示的对象就是标准的JavaScript语言的对象，JSON和Python内置的数据类型对应如下
'''
#time 是外部模块 http://www.jb51.net/article/75364.htm

import asyncio, os, json, time
#datetime外部模块 是Python处理日期和时间的标准库。 注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类。
from datetime import datetime
#从aiohttp内导入web这个函数,
'''
如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。
asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。
'''
from aiohttp import web
#index函数，接收request参数，返回一个web body

from jinja2 import Environment, FilesystemLoader
'''
jinja2 是前端模板引擎  jinja日语神社的意思
沙箱执行模式，模板的每个部分都在引擎的监督之下执行，模板将会被明确地标记在白名单或黑名单内，这样对于那些不信任的模板也可以执行
Jinja2 使用一个名为 Environment 的中心对象。这个类的实例用于存储配 置、全局对象，并用于从文件系统或其它位置加载模板。即使你通过:class:Template 类的构造函数用字符串创建模板，也会为你自动创建一个环境，尽管是共享的。大多数应用在应用初始化时创建一个 Environment 对象，并用它加载模板。 
这里FileSystemLoader是一个模板加载器中的一种，它表示从指定的文件夹中加载模板文件。另外，Jinja2还有很多其他的内置模板，比如PackageLoader、MoudleLoader等等。当然用户还可以自定义模板加载器（只需要继承BaseLoader并重载get_source函数）
'''

import orm
#ORM 数据处理  ORM（Object Relational Mapping）框架采用元数据来描述对象一关系映射细节，元数据一般采用XML格式，并且存放在专门的对象一映射文件中。

from coroweb import add_routes, add_static
#url处理函数是如何注册的   看一下coroweb.py中的add_routes函数  add_routes不是用来注册url处理函数的吗？为什么到现在还没有注册？
#看一下aiohttp官方文档是怎么注册一个url处理函数的


def init_jinja2(app, **kw):
		logging.info('init jinja2...')
		options = dict(
				autoescape =kw.get('autoescape', True),
				block_start_string = kw.get('block_start_string', '{%'),
				block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    }
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env
    
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return (await handler(request))
    return logger

async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data
    
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response
    
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

'''
用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

把@asyncio.coroutine替换为async；
把yield from替换为await。
'''
#协程函数 init
async def init(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='www', password='www', db='awesome')
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv
    
       

		
'''
用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

把@asyncio.coroutine替换为async；
把yield from替换为await。
'''

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