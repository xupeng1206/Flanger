"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""
import datetime
import os

from .exceptions import MethodNotImplement, UrlNotFound, SQLError
from flask import send_file
from sqlalchemy.sql import sqltypes


class SmartResource:
    """
    用当做基础的resource, 目前暂无用处。
    """

    model = None

    def __init__(self, model):
        self.model = model

    def _transform_param(self, type, value):
        # TODO, try except
        if isinstance(type, sqltypes.Integer):
            return int(value)
        if isinstance(type, sqltypes.String):
            return str(value)
        if isinstance(type, sqltypes.DateTime):
            # 约定 timestamp
            try:
                val_float = float(value)
            except Exception:
                # 失败按字符串比较
                return str(value)
            return datetime.datetime.fromtimestamp(val_float)
        # TODO, 兼容各种字段属性
        # 都不满足字符串输出
        return str(value)

    def get(self, request, *args, **kwargs):
        """
        get api
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def _get(self, request, *args, **kwargs):
        qf = []
        for field in self.model.__table__.columns:
            field_name = field.name
            field_exp = getattr(self.model, field_name)

            if field_name in kwargs:
                qf.append(field_exp==self._transform_param(field_exp.type, kwargs[field_name]))
            if f"{field_name}_s" in kwargs:
                qf.append(field_exp.in_(self._transform_param(field_exp.type,kwargs[field_name])))
            if f"{field_name}_lr" in kwargs:
                qf.append(field_exp>=self._transform_param(field_exp.type,kwargs[field_name][0]))
                qf.append(field_exp<=self._transform_param(field_exp.type,kwargs[field_name][1]))
            if f"{field_name}_nlr" in kwargs:
                qf.append(field_exp>self._transform_param(field_exp.type,kwargs[field_name][0]))
                qf.append(field_exp<self._transform_param(field_exp.type,kwargs[field_name][1]))
            if f"{field_name}_l" in kwargs:
                qf.append(field_exp >= self._transform_param(field_exp.type,kwargs[field_name][0]))
                qf.append(field_exp < self._transform_param(field_exp.type,kwargs[field_name][1]))
            if f"{field_name}_r" in kwargs:
                qf.append(field_exp > self._transform_param(field_exp.type,kwargs[field_name][0]))
                qf.append(field_exp <= self._transform_param(field_exp.type,kwargs[field_name][1]))

        lst = self.model.query.order_by(self.model.id).filter(*qf) if len(qf) else self.model.query.order_by(self.model.id).all()
        return [x.to_dict() for x in lst]

    def post(self, request, *args, **kwargs):
        """
        post api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def _post(self, request, *args, **kwargs):
        try:
            attrs = {}
            for k, v in kwargs.items():
                if k in self.model.__table__.columns and k not in ["id", "create_at", "update_at"]:
                    attrs[k] = v
            self.model(**attrs).create()
        except Exception as e:
            raise SQLError
        return {}

    def put(self, request, *args, **kwargs):
        """
        put api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def _put(self, request, id, *args, **kwargs):
        try:
            instance = self.model.query.filter(getattr(self.model, "id")==id).first()
            if instance:
                for k, v in kwargs.items():
                    if k in self.model.__table__.columns and k not in ["id", "create_at", "update_at"]:
                        setattr(instance, k, v)
                instance.update()
        except Exception as e:
            raise SQLError
        return {}

    def delete(self, request, id, *args, **kwargs):
        """
        delete api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def _delete(self, request, id, *args, **kwargs):
        try:
            self.model.delete_filtered(getattr(self.model, "id")==id)
        except Exception as e:
            raise SQLError
        return {}

class SwaggerResource:
    """
    swagger对应的resource，主要用来返回swagger_index.html

    """

    def get(self, debug, *args, **kwargs):
        """
        get方法 返回swagger_index.html
        :param debug:
        :param args:
        :param kwargs:
        :return:
        """
        if debug:
            # debug模式下展现swagger界面
            import flanger
            return send_file(os.path.join(flanger.__swagger__, 'swagger_index.html'))
        else:
            # 生产模式下 不提供swagger
            raise UrlNotFound
