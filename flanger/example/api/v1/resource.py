"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""


class HelloResource:
    """
    这个部分会显示在swagger页面HelloResource分组的描述里
    """

    def get(self, request, *args, **kwargs):
        """
        这里对应 /api/v1/hello的GET方法

        这个部分会显示在 swagger页面/api/v1/hello的GET方法的描述中
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 你可以在这里写这个接口的具体逻辑，最后返回一个dict或一个list即可
        return {'data': 'hello api v1 method GET !!!'}

    def post(self, request, *args, **kwargs):
        """
        这里对应 /api/v1/hello的POST方法

        这个部分会显示在 swagger页面/api/v1/hello的POST方法的描述中
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 你可以在这里写这个接口的具体逻辑，最后返回一个dict或一个list即可
        return {'data': 'hello api v1 method POST !!!'}

    def put(self, request, *args, **kwargs):
        """
        这里对应 /api/v1/hello的PUT方法

        这个部分会显示在 swagger页面/api/v1/hello的PUT方法的描述中
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 你可以在这里写这个接口的具体逻辑，最后返回一个dict或一个list即可
        return {'data': 'hello api v1 method PUT !!!'}

    def delete(self, request, *args, **kwargs):
        """
        这里对应 /api/v1/hello的DELETE方法

        这个部分会显示在 swagger页面/api/v1/hello的DELETE方法的描述中
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 你可以在这里写这个接口的具体逻辑，最后返回一个dict或一个list即可
        return {'data': 'hello api v1 method DELETE !!!'}
