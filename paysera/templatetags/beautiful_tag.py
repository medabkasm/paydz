from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def message_filter(message):
    #message = '<p>{}</p>'.format(message)
    return str(message)
