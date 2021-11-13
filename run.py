from wsgiref.simple_server import make_server

from origina_framework.main import Origin
from urls import routes

application = Origin(routes)


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
