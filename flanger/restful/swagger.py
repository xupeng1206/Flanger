"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

import json
import inspect
import os
from flanger.db.mixin import AutoApiModelMixin
from flanger.keywords import *


def generate_swagger_json(app):
    """
    根据resource的具体情况，自动生成对应的swagger.json文件
    swagger原理；  实际上swagger_index.html的渲染完全由swagger.json决定，只要根据缩写的具体api来生成swagger.json
    就能自动的获得swagger文档，通过学习swagger.json内数据结果代表意义，配合python的自省就能得到对应的swagger.json
    这一函数就是做了这个事情

    :param app:  flanger核心对象
    :return:
    """
    flanger_path = os.path.dirname(os.path.dirname(__file__))
    swagger_ori_path = os.path.join(os.path.join(flanger_path, 'swagger'), 'swagger_ori.json')

    with open(swagger_ori_path, 'r') as load_f:
        load_dict = json.load(load_f)

    # swagger doc setting start
    load_dict["info"]["description"] = ""
    load_dict["info"]["version"] = '0.0.0'
    load_dict["info"]["title"] = "Flanger Swagger Document"
    load_dict["host"] = ""
    load_dict["basePath"] = ""
    # swagger doc setting end

    # if hasattr(app.config, "SWAGGER_EXCLUDE_PARAMS"):
    if SWAGGER_IGNORE_PARAMS in app.config:
        exclude_params = ["self", "request"] + app.config['SWAGGER_IGNORE_PARAMS']
    else:
        exclude_params = ["self", "request"]
    exclude_params = list(set(exclude_params))

    # generate json for swagger
    for k, v in app.endpoint_resource.items():  # app.endpoint_resource 里面有全部注册的resource
        cls_path_dict = dict()

        if v.__doc__:
            tag_description = v.__doc__
        else:
            tag_description = ''

        load_dict["tags"].append({
            "name": app.endpoint_url[k],         # 用url做这个resource的名字 更直观一点
            "description": tag_description,      # 用resource的__doc__做描述 写resource的时候  可以简要概述 这个resource是做啥用的
            "externalDocs": {'description': k}   # 这里用endpoint作为分类行右侧小说明
        })

        # GET 方法
        if "get" in v.allowed_methods:
            cls_path_dict["get"] = {}
            cls_path_dict["get"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["get"]["summary"] = f"{app.endpoint_url[k]} get method"
            cls_path_dict["get"]["description"] = v.get.__doc__   # method的doc string 作为描述， 可以将方法使用，参数说明在这里体现
            cls_path_dict["get"]["parameters"] = []
            get_params_in_code = inspect.getfullargspec(v.get).args
            if getattr(v, 'model', None) in AutoApiModelMixin.__subclasses__():
                get_params_in_code.extend([x.name for x in getattr(v, "model").__table__.columns if x.name not in ["id", "create_at", "update_at"]])
            get_params = [x for x in get_params_in_code if x not in exclude_params]
            annotations = v.get.__annotations__
            defaults = v.get.__defaults__
            # 这里需要考虑参数annotations和defaults个数不匹配
            num = len(get_params) - len(defaults) if defaults else len(get_params)
            for index, param in enumerate(get_params):
                param_dict = dict()
                param_dict['name'] = param
                param_dict['in'] = "query"
                param_dict['description'] = ''
                # int和float类型转换为swagger对应的integer和number,其余类型在swagger中没有对应的，保持原样
                if param in annotations.keys():
                    if annotations[param].__name__ == 'int':
                        param_dict['type'] = 'integer'
                    elif annotations[param].__name__ == 'float':
                        param_dict['type'] = 'number'
                    else:
                        param_dict['type'] = annotations[param].__name__
                if index >= num:
                    param_dict['default'] = defaults[index - num]
                cls_path_dict["get"]["parameters"].append(param_dict)

            cls_path_dict["get"]["responses"] = {}

        # POST 方法
        if "post" in v.allowed_methods:
            cls_path_dict["post"] = {}
            cls_path_dict["post"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["post"]["summary"] = f"{app.endpoint_url[k]} post method"
            cls_path_dict["post"]["description"] = v.post.__doc__
            cls_path_dict["post"]["parameters"] = []
            post_params_in_code = inspect.getfullargspec(v.post).args
            if getattr(v, 'model', None) in AutoApiModelMixin.__subclasses__():
                post_params_in_code.extend([x.name for x in getattr(v, "model").__table__.columns if x.name not in ["id", "create_at", "update_at"]])
            post_params = [x for x in post_params_in_code if x not in exclude_params]
            annotations = v.post.__annotations__

            isfile = False
            for param in post_params:
                if param in annotations.keys():
                    if annotations[param].__name__ == 'File':
                        isfile = True
                        break
            if isfile:
                cls_path_dict["post"]["consumes"] = ['multipart/form-data']
                for param in post_params:
                    param_dict = dict()
                    param_dict['name'] = param
                    param_dict['in'] = "formData"
                    param_dict['description'] = ""
                    if param in annotations.keys():
                        if annotations[param].__name__ == 'File':
                            param_dict['type'] = "file"
                    cls_path_dict["post"]["parameters"].append(param_dict)
            else:
                defaults = v.post.__defaults__
                num = len(post_params) - len(defaults) if defaults else len(post_params)
                param_dict = dict()
                param_dict['name'] = "parameters"
                param_dict['in'] = "body"
                param_dict['description'] = ""
                param_dict['schema'] = {}
                properties = {}
                for index, param in enumerate(post_params):
                    if param in annotations.keys():
                        if annotations[param].__name__ == 'int':
                            param_type = 'integer'
                        elif annotations[param].__name__ == 'float':
                            param_type = 'number'
                        else:
                            param_type = annotations[param].__name__
                    else:
                        # 如果参数没有annotation，则为string类型，因为此处必须赋类型
                        param_type = "string"
                    if index >= num:
                        param_default = defaults[index - num]
                        properties[param] = {"type": param_type, "default": param_default}
                    else:
                        properties[param] = {"type": param_type}
                param_dict['schema']["properties"] = properties
                cls_path_dict["post"]["parameters"].append(param_dict)

            cls_path_dict["post"]["responses"] = {}

        # PUT 方法
        if "put" in v.allowed_methods:
            cls_path_dict["put"] = {}
            cls_path_dict["put"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["put"]["summary"] = f"{app.endpoint_url[k]} put method"
            cls_path_dict["put"]["description"] = v.put.__doc__
            cls_path_dict["put"]["parameters"] = []
            put_params_in_code = inspect.getfullargspec(v.put).args
            if getattr(v, 'model', None) in AutoApiModelMixin.__subclasses__():
                put_params_in_code.extend([x.name for x in getattr(v, "model").__table__.columns if x.name not in ["id", "create_at", "update_at"]])
            put_params = [x for x in put_params_in_code if x not in exclude_params]
            annotations = v.put.__annotations__

            isfile = False
            for param in put_params:
                if param in annotations.keys():
                    if annotations[param].__name__ == 'File':
                        isfile = True
                        break
            if isfile:
                cls_path_dict["put"]["consumes"] = ['multipart/form-data']
                for param in put_params:
                    param_dict = dict()
                    param_dict['name'] = param
                    param_dict['in'] = "formData"
                    param_dict['description'] = ""
                    if param in annotations.keys():
                        if annotations[param].__name__ == 'File':
                            param_dict['type'] = "file"
                    cls_path_dict["put"]["parameters"].append(param_dict)
            else:
                defaults = v.put.__defaults__
                num = len(put_params) - len(defaults) if defaults else len(put_params)
                param_dict = dict()
                param_dict['name'] = "parameters"
                param_dict['in'] = "body"
                param_dict['description'] = ""
                param_dict['schema'] = {}
                properties = {}
                for index, param in enumerate(put_params):
                    if param in annotations.keys():
                        if annotations[param].__name__ == 'int':
                            param_type = 'integer'
                        elif annotations[param].__name__ == 'float':
                            param_type = 'number'
                        else:
                            param_type = annotations[param].__name__
                    else:
                        # 如果参数没有annotation，则为string类型，因为此处必须赋类型
                        param_type = "string"
                    if index >= num:
                        param_default = defaults[index - num]
                        properties[param] = {"type": param_type, "default": param_default}
                    else:
                        properties[param] = {"type": param_type}
                param_dict['schema']["properties"] = properties
                cls_path_dict["put"]["parameters"].append(param_dict)

            cls_path_dict["put"]["responses"] = {}

        # DELETE 方法
        if "delete" in v.allowed_methods:
            cls_path_dict["delete"] = {}
            cls_path_dict["delete"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["delete"]["summary"] = f"{app.endpoint_url[k]} delete method"
            cls_path_dict["delete"]["description"] = v.delete.__doc__
            cls_path_dict["delete"]["parameters"] = []
            delete_params_in_code = inspect.getfullargspec(v.delete).args
            delete_params = [x for x in delete_params_in_code if x not in exclude_params]
            annotations = v.delete.__annotations__
            defaults = v.delete.__defaults__
            # 这里需要考虑参数annotations和defaults个数不匹配
            num = len(delete_params) - len(defaults) if defaults else len(delete_params)
            for index, param in enumerate(delete_params):
                param_dict = dict()
                param_dict['name'] = param
                param_dict['in'] = "query"
                param_dict['description'] = ''
                # int和float类型转换为swagger对应的integer和number,其余类型在swagger中没有对应的，保持原样
                if param in annotations.keys():
                    if annotations[param].__name__ == 'int':
                        param_dict['type'] = 'integer'
                    elif annotations[param].__name__ == 'float':
                        param_dict['type'] = 'number'
                    else:
                        param_dict['type'] = annotations[param].__name__
                if index >= num:
                    param_dict['default'] = defaults[index - num]
                cls_path_dict["delete"]["parameters"].append(param_dict)

            cls_path_dict["delete"]["responses"] = {}

        load_dict["paths"][f"{app.endpoint_url[k]}"] = cls_path_dict

    # 找到app 所在的目录 将新的json文件写在app项目目录下比较合适
    web_statics_folder = os.path.join(f'{app.config["BASE_DIR"]}', 'static')
    json_file_path = os.path.join(web_statics_folder, 'swagger.json')

    if not os.path.exists(web_statics_folder):
        os.mkdir(web_statics_folder)
    with open(json_file_path, 'w+') as dump_f:
        json.dump(load_dict, dump_f)
