from flanger.restful.resource import BaseResource

class HelloWorld(BaseResource):

    def get(self, *args, **kwargs):
        return {'hello': 'world'}
