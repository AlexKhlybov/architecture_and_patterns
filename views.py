from origina_framework.templator import render


class Index:
    def __call__(self):
        return '200 OK', render('index.html')


class Portfolio:
    def __call__(self):
        return '200 OK', render('portfolio.html')


class Services:
    def __call__(self):
        return '200 OK', render('services.html')
