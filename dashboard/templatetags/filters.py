from babel import numbers
from django import template

register = template.Library()


@register.filter
def format(value):
    formated_value = ''
    try:
        formated_value = numbers.format_currency(value, 'BRL', locale='pt_BR')
    except Exception:
        formated_value = 'R$ 00,00'

    return formated_value
