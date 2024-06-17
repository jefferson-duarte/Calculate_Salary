from django.template import Library
from utils import utils

register = Library()


@register.filter
def price_format(price):
    return utils.price_format(price)


@register.filter
def one_float(value):
    return utils.one_float(value)
