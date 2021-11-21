from views import Index, Portfolio, Services

routes = {
    '/': Index(),
    '/portfolio/': Portfolio(),
    '/services/': Services()
}
