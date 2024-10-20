from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, args):
    """
    Replaces the first value with the second value in the string.
    Example: {{ string|replace:“{i},new_value” }}
    """
    old, new = args.split(',')
    return value.replace(old, new)
