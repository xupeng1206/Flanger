class BaseAppMiddleWare:

    def process_request(self, request):
        print('before_request')
