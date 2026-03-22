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
    }, {
        'name': 'Contact Us',
        'href': '/contact',
        'icon': 'fa-paper-plane',
    }, {
        'name': 'About Us',
        'href': '/about',
        'icon': 'fa-address-card',
    },{
        'name': 'News',
        'href': '/news/',
        'icon': 'fa-newspaper',
    },{
        'name': 'Add news',
        'href': '/news/create',
        'icon': 'fa-plus',
    },{
        'name': 'Forum',
        'href': '/forum',
        'icon': 'fa-comment', #look for your icon here https://fontawesome.com/search?ic=free
    }]
    