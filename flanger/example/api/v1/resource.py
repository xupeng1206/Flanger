class HelloResource:

    def get(self, request, *args, **kwargs):
        return {'version': 'hello api v1 !!!'}
