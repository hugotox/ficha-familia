from datetime import datetime
from django import template
from settings import STATIC_FILES_VERSION
register = template.Library()


@register.filter(name='zfill')
def zfill(value, digits):
    return str(value).zfill(digits)

@register.simple_tag
def get_static_version():
    return STATIC_FILES_VERSION


@register.simple_tag
def get_date_now(format="%d/%m/%Y"):
    return datetime.now().strftime(format)

