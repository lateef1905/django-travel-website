from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the arg to the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
