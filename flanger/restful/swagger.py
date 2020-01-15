"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

import json
import inspect
import os


def generate_swagger_json(app):
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
    if "SWAGGER_IGNORE_PARAMS" in app.config:
        exclude_params = ["self", "request"] + app.config['SWAGGER_IGNORE_PARAMS']
    else:
        exclude_params = ["self", "request"]

    # generate json for swagger
    for k, v in app.endpoint_resource.items():
        cls_path_dict = dict()

        if v.__doc__:
            tag_description = v.__doc__
        else:
            tag_description = ''
        load_dict["tags"].append({
            "name": app.endpoint_url[k],
            "description": tag_description
        })
        if "get" in v.allowed_methods:
            cls_path_dict["get"] = {}
            cls_path_dict["get"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["get"]["summary"] = f"{app.endpoint_url[k]} get method"
            cls_path_dict["get"]["description"] = v.get.__doc__
            cls_path_dict["get"]["parameters"] = []
            get_params_in_code = inspect.getfullargspec(v.get).args
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

        if "post" in v.allowed_methods:
            cls_path_dict["post"] = {}
            cls_path_dict["post"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["post"]["summary"] = f"{app.endpoint_url[k]} post method"
            cls_path_dict["post"]["description"] = v.post.__doc__
            cls_path_dict["post"]["parameters"] = []
            post_params_in_code = inspect.getfullargspec(v.post).args
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

        if "put" in v.allowed_methods:
            cls_path_dict["put"] = {}
            cls_path_dict["put"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["put"]["summary"] = f"{app.endpoint_url[k]} put method"
            cls_path_dict["put"]["description"] = v.put.__doc__
            cls_path_dict["put"]["parameters"] = []
            put_params_in_code = inspect.getfullargspec(v.put).args
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

        if "delete" in v.allowed_methods:
            cls_path_dict["delete"] = {}
            cls_path_dict["delete"]["tags"] = [app.endpoint_url[k]]
            cls_path_dict["delete"]["summary"] = f"{app.endpoint_url[k]} delete method"
            cls_path_dict["delete"]["description"] = v.delete.__doc__
            cls_path_dict["delete"]["parameters"] = []
            delete_params_in_code = inspect.getfullargspec(v.delete).args
            delete_params = [x for x in delete_params_in_code if x not in delete_params_in_code]
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

    web_statics_folder = os.path.join(f'{app.config["BASE_DIR"]}', 'static')
    json_file_path = os.path.join(web_statics_folder, 'swagger.json')
    if not os.path.exists(web_statics_folder):
        os.mkdir(web_statics_folder)
    with open(json_file_path, 'w+') as dump_f:
        json.dump(load_dict, dump_f)

