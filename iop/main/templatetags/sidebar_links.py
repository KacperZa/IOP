from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [{
        'name': 'Home',
        'href': '/',
        'icon': 'fa-house',
    }, {
        'name': 'My Listings',
        'href': '/cars',
        'icon': 'fa-car',
    },{
        'name': 'New Listings',
        'href': '/news/',
        'icon': 'fa-newspaper',
    },{
        'name': 'Add Listing',
        'href': '/news/create',
        'icon': 'fa-plus',
    }]
    