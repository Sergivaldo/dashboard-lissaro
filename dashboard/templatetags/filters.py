from django import template

from dashboard.utils.utils import format_value

register = template.Library()


@register.filter
def format(value):
    return format_value(value)

