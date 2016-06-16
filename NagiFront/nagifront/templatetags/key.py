from django.template import Library

register = Library()

def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)
