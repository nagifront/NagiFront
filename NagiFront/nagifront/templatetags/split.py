from django.template import Library

register = Library()

def split(s):
    if s is not None:
        return s.split(',')
    else:
        return None
key = register.filter('split', split)
