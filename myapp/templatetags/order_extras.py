# myapp/templatetags/order_extras.py
from django import template

register = template.Library()

@register.filter
def total_price(order_items):
    return sum(item.total for item in order_items)
