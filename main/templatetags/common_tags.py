from datetime import datetime
from django import template
from main.models import Familia
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


@register.simple_tag
def get_estado_familia(familia, anio):
    if isinstance(familia, Familia):
        return familia.get_estado(False, anio)
    else:
        return ""

@register.simple_tag
def get_color_btn_ficha(persona, anio):
    return persona.get_color_btn_ficha(anio)