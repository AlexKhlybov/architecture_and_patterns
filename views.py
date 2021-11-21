from components.routers import AppRoute
from origina_framework.templator import render

routes = {}


@AppRoute(routes=routes, url="/")
class Index:
    def __call__(self, request):
        return "200 OK", render("index.html")


@AppRoute(routes=routes, url="/portfolio/")
class Portfolio:
    def __call__(self, request):
        return "200 OK", render("portfolio.html")


@AppRoute(routes=routes, url="/services/")
class Services:
    def __call__(self, request):
        return "200 OK", render("services.html")
