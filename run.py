from wsgiref.simple_server import make_server

from components import settings
from origina_framework.main import Origin
from views import routes

application = Origin(settings, routes)


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
