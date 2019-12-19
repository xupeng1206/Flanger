class HelloResource:

    def get(self, request, *args, **kwargs):
        return {'version': 'v1'}