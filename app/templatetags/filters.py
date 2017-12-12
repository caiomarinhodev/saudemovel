from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(float(float(value)/float(arg))* 100)
    except (ValueError, ZeroDivisionError):
        return None
