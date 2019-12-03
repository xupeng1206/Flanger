from flanger.restful.resource import BaseResource


class HelloResource(BaseResource):

    def get(self, *args, **kwargs):
        return {}