import quopri
from os import path

from components.content_types import CONTENT_TYPES_MAP
from views import FakeViews

from .requests import GetRequests, PostRequests
from .responce import Status


class PageNotFound404:
    def __call__(self):
        return Status.HTTP_404_NOT_FOUND()


class Origin:
    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if method == "POST":
            data = PostRequests().get_request_params(environ)
            request["data"] = data
            print(f"Нам пришел POST-запрос : {Origin.decode_value(data)}")
        if method == "GET":
            request_params = GetRequests().get_request_params(environ)
            request["request_params"] = request_params
            print(f"Нам пришли GET-параметры: {request_params}")

        if path in self.routes_lst:
            view = self.routes_lst[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode("utf-8")
        elif path.startswith(self.settings.STATIC_URL):
            file_path = path[len(self.settings.STATIC_URL): len(path) - 1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(
                self.settings.STATIC_FILES_DIR, file_path
            )
        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view()
            body = body.encode("utf-8")
        start_response(code, [("Content-Type", content_type)])
        return [body]

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        extension = path.splitext(file_name)[1]
        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, "rb") as f:
            file_content = f.read()
        status_code = Status.HTTP_200_OK()
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace("%", "=").replace("+", " "), "UTF-8")
            val_decode_str = quopri.decodestring(val).decode("UTF-8")
            new_data[k] = val_decode_str
        return new_data


class FakeOrigin:
    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        view = FakeViews()
        content_type = Origin.get_content_type(path)
        code, body = view()
        body = body.encode("utf-8")
        start_response(code, [("Content-Type", content_type)])
        return [body]
