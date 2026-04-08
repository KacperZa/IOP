from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [{
        'name': 'Dom',
        'href': '/',
        'icon': 'fa-house',
    }, {
        'name': 'Moje ogłoszenia',
        'href': '/cars',
        'icon': 'fa-car',
    },{
        'name': 'Ogłoszenia',
        'href': '/news/',
        'icon': 'fa-newspaper',
    },{
        'name': 'Dodaj ogłoszenie',
        'href': '/news/create',
        'icon': 'fa-plus',
    }]
    