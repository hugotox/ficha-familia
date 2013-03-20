from django import template
from FichaFamilia.settings import STATIC_FILES_VERSION
register = template.Library()


@register.filter(name='zfill')
def zfill(value, digits):
    return str(value).zfill(digits)

@register.simple_tag
def get_static_version():
    return STATIC_FILES_VERSION
