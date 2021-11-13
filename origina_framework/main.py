class PageNotFound404:
    def __call__(self):
        return '404 WHAT', '404 PAGE Not Found'


class Origin:

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
