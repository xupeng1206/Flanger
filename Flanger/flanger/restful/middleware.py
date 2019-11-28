class BaseAppMiddleWare:

    def before_first_request(self, request, session, g, app):
        print('before_first_request')

    def before_request(self, request, session, g, app):
        print('before_request')

    def after_request(self, response):
        print('after_request')
        return response

    def teardown_request(self, e):
        print('teardown_request')
        pass