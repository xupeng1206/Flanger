# Flanger

一个基于flask的restful api框架。自带swagger的功能，无须自己写，简化了参数解析，方便快速构建api!!!

# 一. 安装框架
## 安装

```
git clone https://github.com/xupeng1206/Flanger.git
cd Flanger
python intall.py 或者 python setup.py install
```
    
## 验证

进入python shell
```
>>import flanger
>>flanger.__version__
// '0.0.1' 
```
    
# 二. 快速开始
## 创建示例服务
```
1.在任意位置，输入Flanger create_project <你的项目名称>, 即可生成示例代码！
2.进入项目目录：cd <你的项目名称>
3.启动后台服务：python manage.py
4.浏览器访问GET http://127.0.0.1:8080/api/v1/hello
```
## 快速新增一个api
1. 在<你的项目名称>/api/v1/resource.py，新增一个类
```
class NewResource:

    def get(self, request, *args, **kwargs):   # GET方法的逻辑
        return {'data':'new get api !!!'}

```
2. 在<你的项目名称>/api/v1/urls.py中V1Urls中urls属性中新增如一行绑定，如下：
```
from .resource import NewResource

class V1Urls:

    # url_prefix 属性可以没有
    url_prefix = '/api/v1'

    # urls属性必须要有
    urls = {
        # key: url, value: resource
        '/hello': HelloResource,
        # 可以在下面添加自己的url及对应的resource
        # ...
        '/new': NewResource,  # 新增的api路由

    }
```
3.至此，api新增完毕，可浏览器GET访问 http://127.0.0.1:8080/api/v1/new 

# 三. 各个部分详细介绍
## 1. settings：
就是普通的flask的settings文件，或者叫config文件，名称啥的随意，最后都是用来fromobject的，settings中有几个属性：
```
# 常用
# 项目的根目录（必须有的，不然自带的swagger会有问题！）
BASE_DIR = os.path.dirname(__file__)
# 用来注册urls, 是个list
FLANGER_URLS = [
    'api.v1.urls.V1Urls',
    # 'api.v2.urls.V2Urls', ex 如果要新一个class来注册就像这样写
]

# 不常用
# # 用来注册自定义的请求处理器(request processor)，是个list
# # request processor 配置写法和url的类似
# # 功能有点类似django的middlewave中处理request的部分
FLANGER_REQUEST_PROCESSORS = []

# # 用来注册自定义的response处理器，是个list
# # response processor 配置写法和url的类似
# # 功能有点类似django的middlewave中处理response的部分
FLANGER_RESPONSE_PROCESSORS = [] 

# # swagger忽略的params列表, 比如token之类的
# # 正常在resource的（get post put delete）方法中的参数除了request，args,kwargs是不会被识别到api的参数
# # 如果你不想token被识别，则在下面列表中加入 ‘token’  ( --> ['token'] ), 这样token就不会被显示成api的参数
SWAGGER_IGNORE_PARAMS = [] 

# 其他
flask的其他属性都可以写在这里

```
## 2. resource：
表示资源，比如BookResource表示服务端的书籍资源，BookResource类下面的get方法，可以表示获取服务端的书籍资源的方法（就是一个api），
具体的逻辑就可以写在这个get方法下面，同理还有post,put,delete方法，简单讲一个resource可以有种方法对应四个api方法。

```
ex:


class BookResource:

    def get(self, request, name, author='雨果', *args, **kwargs):
        # 根据name,author去数据库查询
        # do sql or orm select
        return {'data': {
            'id'：xxx,
            'name': xxx,
            'author': xxx,
            'pub-date': xxx,
            ....
        }}
        
在这个例子中，定义了一个HTTP GET方法，参数有name和author,url传参或是json传参无论啥形式，
写后端业务的可以不用去关心（无论啥，框架都会解析出来，分发到各自方法的参数上去）
```

## 3. urls：
url注册模块的作用是将resource和urls绑定，使之可以通过HTTP方法访问不用的url,执行不同resource下的不同方法。

```
示范代码：

from .resource import HelloResource


class V1Urls:
    """
    类名随便取都行

    属性：
    1. url_prefix (可以没有)
        url的前缀，给这个类底下涉及的url都套上前缀, 如下面的 /hello会被注册成  /api/v1/hello, 若果没有url_prefix属性, /hello 会被注册成 /hello

    2. urls (必要属性，类型是dict)
        key:    url路径（flask中注册路径怎么写，这里就怎么写,如：/hello, /hello/<name> 等）
        value:  url对应的resource

        注：    这写url和resource对应关系时候，不用关心method和endpoint, 交由框架去处理

    重点：
        要想这个类有有效，一定要在settings的FLANGER_URLS中注册
    """

    # url_prefix 属性可以没有
    url_prefix = '/api/v1'

    # urls属性必须要有
    urls = {
        # key: url, value: resource
        '/hello': HelloResource,
        # 可以在下面添加自己的url及对应的resource
        # ...

    }

    
要想将2中新建的resource,绑定对应的url，只需两步
1. 在文件头的部分引入对应的resource
      from .resource import BookResource
2. 在urls 中新增一行：
      ‘/book’ : BookResource,
```

## 4. manage:
这个部分其实没啥就是实例化一下flanger的核心对象app
```
# 引入FlangerApp
from flanger.app import FlangerApp

# 实例化FlangerApp (Flanger核心对象)，当Flask一样用就行
app = FlangerApp(__name__)

# 给app写入配置文件 (当Flask一样用)
app.config.from_object('settings')

# 初始化Flanger的功能（必须在导入配置之后init）
app.init()

# ORM，Migrate, Script 等flask的插件 该怎么用仍然怎么用

if __name__ == '__main__':
    # 启动开发服务器
    app.run(debug=True, port=8080)

```

## 5. swagger:
1. 框架自带的swagger，注册过的resource,会自动创建对应的swagger条目，swagger页面中api的参数内容就是，resource下对应方法的参数，
除了request，args, kwargs和SWAGGER_IGNORE_PARAMS列表中的内容
2. swagger页面的访问方式： HTTP GET  /swagger


## 6. request processor：
可以自定义，但是必须知道flanger的内部原理，最好看过源码，这里不介绍了。请自行学习源码。

## 7. response processor：
可以自定义，但是必须知道flanger的内部原理，最好看过源码，这里不介绍了。请自行学习源码。

## 8. 命令
    1）. Flanger create_project <你的项目名称>：
        创建项目工程，生成示范代码。

# 四. 建议
说明相对较简单，建议看一下示范代码和源码！

# 五. 联系我

有问题请联系我：
```
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206
QQ          874582705
```