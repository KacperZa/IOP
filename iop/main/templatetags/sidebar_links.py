from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [{
        'name': 'Strona Główna',
        'href': '/',
        'icon': 'fa-house',
    }, {
        'name': 'Moje ogłoszenia',
        'href': '/cars',
        'icon': 'fa-book-open',
    },{
        'name': 'Ogłoszenia',
        'href': '/news/',
        'icon': 'fa-inbox',
    },{
        'name': 'Dodaj ogłoszenie',
        'href': '/news/create',
        'icon': 'fa-plus',
    }]
    