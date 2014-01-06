# -*- encoding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils import simplejson
from main.models import CentroFamiliar, FactorProtector
from main.reports_helper import *
from utils.json_utils import json_response
from datetime import datetime


@login_required
def home(request, anio=None):

    if anio is None:
        anio = datetime.now().year

    active = 'cantidad_fichas'

    # conteo de familias por centro
    count_familias = get_familias_por_centro()

    # conteo de personas por centro
    datos = get_personas_por_centro()

    # conteo de fichas activas
    fichas_activas = get_conteo_fichas_por_centro(anio)

    # agregar el conteo de familias y fichas activas
    for c1 in datos:
        for c2 in count_familias:
            if c2['centro_familiar__comuna'] == c1['comuna']:
                c1['count_familias'] = c2['count']
                c1['fichas_activas'] = 0
                break

    # agregar el conteo de fichas activas
    for c1 in datos:
        for c2 in fichas_activas:
            if c2['comuna'] == c1['comuna']:
                c1['fichas_activas'] = c2['count_fichas']
                break

    # calcular totales
    total_familias = 0
    total_personas = 0
    total_fichas_activas = 0
    for c in datos:
        total_familias += c['count_familias']
        total_personas += c['count_personas']
        total_fichas_activas += c['fichas_activas']

    return render(request, 'reportes/cantidad_fichas.html', locals())


@login_required
def cantidad_fichas(request, anio, tipo):
    grafico_cobertura = ''

    if tipo == 'familias':
        count_familias = get_familias_por_centro()

        grafico_cobertura = {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': 'Cobertura'
            },
            'xAxis': {
                'categories': [x['centro_familiar__comuna'] for x in count_familias]
            },
            'yAxis': {
                'title': {
                    'text': 'Cobertura'
                }
            },
            'series': [
                {
                    'name': 'Total Familias',
                    'data': [x['count'] for x in count_familias]
                }
            ]
        }

    elif tipo == 'personas':

        datos = get_personas_por_centro()

        grafico_cobertura = {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': 'Personas/Fichas Activas'
            },
            'xAxis': {
                'categories': [x['comuna'] for x in datos]
            },
            'yAxis': {
                'title': {
                    'text': 'Cobertura'
                }
            },
            'series': [
                {
                    'name': 'Total Personas',
                    'data': [x['count_personas'] for x in datos]
                }
            ]
        }

    elif tipo == 'fichas':

        fichas_activas = get_conteo_fichas_por_centro(anio)

        grafico_cobertura = {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': 'Cobertura'
            },
            'xAxis': {
                'categories': [x['comuna'] for x in fichas_activas]
            },
            'yAxis': {
                'title': {
                    'text': 'Cobertura'
                }
            },
            'series': [
                {
                    'name': 'Total Fichas Activas',
                    'data': [x['count_fichas'] for x in fichas_activas]
                }
            ]
        }

    return json_response(grafico_cobertura)


@login_required
def tipos_familias(request, anio):
    active = 'tipos_familias'
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    mi_centro = user_profile.centro_familiar
    centros = CentroFamiliar.objects.exclude(comuna="Casa Central")
    datos = get_conteo_familias_por_tipo(anio, mi_centro.comuna, True)
    return render(request, "reportes/tipos_familias.html", locals())


@login_required
def estado_ciclos(request, anio):
    active = 'estado_ciclos'
    datos = []
    fichas_cerradas = get_conteo_fichas_por_centro(anio, 'cerradas')
    fichas_activas = get_conteo_fichas_por_centro(anio)
    total_fichas_activas = 0
    total_fichas_cerradas = 0
    for fila_act in fichas_activas:
        for fila_cerr in fichas_cerradas:
            if fila_act['comuna_id'] == fila_cerr['comuna_id']:
                acum = {
                    'comuna_id': fila_act['comuna_id'],
                    'comuna': fila_act['comuna'],
                    'fichas_activas': fila_act['count_fichas'],
                    'fichas_cerradas': fila_cerr['count_fichas']
                }
                datos.append(acum)
                total_fichas_activas += fila_act['count_fichas']
                total_fichas_cerradas += fila_cerr['count_fichas']
                break

    grafico = {
        'chart': {
            'type': 'bar',
            'renderTo': 'div-grafico-estado-ciclos'
        },
        'title': {
            'text': 'Estado de Ciclos'
        },
        'xAxis': {
            'categories': [x['comuna'] for x in datos]
        },
        'yAxis': {
            'title': {
                'text': 'Cantidad de Fichas'
            }
        },
        'series': [
            {
                'name': 'Fichas Activas',
                'data': [x['fichas_activas'] for x in datos]
            },
            {
                'name': 'Fichas Cerradas',
                'data': [x['fichas_cerradas'] for x in datos]
            }
        ]
    }

    grafico = simplejson.dumps(grafico)

    return render(request, 'reportes/estado_ciclos.html', locals())


@login_required
def estado_datos(request, anio):
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'estado_datos'
    centros = CentroFamiliar.objects.exclude(comuna='Casa Central')
    return render(request, 'reportes/estado_datos.html', locals())


@login_required
def rel_familia_persona(request, anio):
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'rel_fam_per'
    datos = get_relacion_familia_ficha(anio)
    return render(request, 'reportes/rel_familia_persona.html', locals())


@login_required
def fichas_por_objetivo(request, anio):
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'fichas_obj'
    datos = get_fichas_por_objetivo(anio)
    return render(request, 'reportes/fichas_objetivo.html', locals())


@login_required
def fichas_por_objetivo_comuna(request, anio, factor_id):
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    datos = get_fichas_por_objetivo_comuna(anio, factor_id)
    return json_response(datos)


@login_required
def condiciones_vulnerabilidad(request, anio):
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404

    active = 'condiciones'

    condiciones = [
        ('cond_precariedad', u'Condiciones de precariedad: vivienda, trabajo, situación sanitaria, otras.'),
        ('cond_vulnerabilidad', u'Vulnerabilidad barrial (inseguridad, violencia, estigma, pocos accesos).'),
        ('cond_hogar_uni_riesgo', u'Hogar unipersonal en situación de riesgo.'),
        ('cond_familia_mono_riesgo', u'Familia monoparental en situación de riesgo.'),
        ('cond_alcohol_drogas', u'Consumo problemático de alcohol y/o drogas.'),
        ('cond_discapacidad', u'Presencia de discapacidad física y/o mental.'),
        ('cond_malos_tratos', u'Experiencias de malos tratos (actual o histórica).'),
        ('cond_socializ_delictual', u'Historial de socialización delictual (detenciones, problemas judiciales).'),
    ]

    totales = []

    for condicion in condiciones:

        presente = get_count_condiciones_vulnerabilidad(condicion[0], 'true')
        no_presente = get_count_condiciones_vulnerabilidad(condicion[0], 'false')
        sin_info = get_count_condiciones_vulnerabilidad(condicion[0], 'null')

        presente = presente[0]['count'] if len(presente) else 0
        no_presente = no_presente[0]['count'] if len(no_presente) else 0
        sin_info = sin_info[0]['count'] if len(sin_info) else 0
        total = presente + no_presente + sin_info

        dato = {
            'condicion': condicion[1],
            'presente': "%s (%s%%)" % (presente, round(presente * 100.0 / total)),
            'no_presente': "%s (%s%%)" % (no_presente, round(no_presente * 100.0 / total)),
            'sin_info': "%s (%s%%)" % (sin_info, round(sin_info * 100.0 / total)),
        }

        totales.append(dato)


    # --- por centro ---

    datos_centros = []

    centros = CentroFamiliar.objects.exclude(comuna='Casa Central')

    for centro in centros:

        datos = []

        for condicion in condiciones:

            presente = get_count_condiciones_vulnerabilidad(condicion[0], 'true', centro.id)
            no_presente = get_count_condiciones_vulnerabilidad(condicion[0], 'false', centro.id)
            sin_info = get_count_condiciones_vulnerabilidad(condicion[0], 'null', centro.id)

            presente = presente[0]['count'] if len(presente) else 0
            no_presente = no_presente[0]['count'] if len(no_presente) else 0
            sin_info = sin_info[0]['count'] if len(sin_info) else 0
            total = presente + no_presente + sin_info

            dato = {
                'condicion': condicion[1],
                'presente': "%s (%s%%)" % (presente, round(presente * 100.0 / total)),
                'no_presente': "%s (%s%%)" % (no_presente, round(no_presente * 100.0 / total)),
                'sin_info': "%s (%s%%)" % (sin_info, round(sin_info * 100.0 / total)),
            }

            datos.append(dato)

        datos_centros.append({'centro': centro.comuna, 'datos': datos})

    return render(request, 'reportes/condiciones.html', locals())


@login_required
def participacion_actividades(request, anio):
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'particip_activ'
    datos, totales = get_participacion_actividades(anio)
    return render(request, 'reportes/particip_activ.html', locals())


@login_required
def actividades_objetivo(request, anio):
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'actividades_objetivo'
    datos = get_participacion_actividades_por_objetivo(anio)
    return render(request, 'reportes/actividades_objetivo.html', locals())

@login_required
def prom_por_factor(request, anio):
    es_admin = request.user.is_superuser
    if not es_admin:
        raise Http404
    active = 'prom_por_factor'
    datos, datos_com = resultados_por_factor(anio)

    centros = CentroFamiliar.objects.exclude(comuna='Casa Central')

    datos_centros = []

    for centro in centros:
        dato, dato_com = resultados_por_factor(anio, centro.id)
        datos_centros.append({
            'centro': centro.comuna,
            'dato': dato,
            'dato_com': simplejson.dumps(dato_com)
        })

    datos_com = simplejson.dumps(datos_com)

    return render(request, 'reportes/promedio_por_factor.html', locals())