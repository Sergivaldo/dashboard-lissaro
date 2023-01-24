from babel import numbers
from django import template

register = template.Library()


@register.filter
def format(value):

    return numbers.format_currency(value, 'BRL', locale='pt_BR')
