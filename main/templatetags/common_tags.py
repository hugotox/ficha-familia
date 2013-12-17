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


@register.simple_tag
def get_porcentaje_completo(centro):
    return round(centro.get_porcentaje_completo(), 2)


@register.simple_tag
def get_porcentaje_completo_p2(centro, anio):
    return round(centro.get_porcentaje_completo_p2(anio), 2)


@register.simple_tag
def get_porcentaje_completo_p2_c(centro, anio):
    return round(centro.get_porcentaje_completo_p2_c(anio), 2)


@register.simple_tag
def get_porcentaje_completo_p3(centro, anio):
    return round(centro.get_porcentaje_completo_p3(anio), 2)