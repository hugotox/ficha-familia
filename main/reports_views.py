from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import simplejson
from main.models import CentroFamiliar
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


def estado_datos(request, anio):
    active = 'estado_datos'
    return render(request, 'reportes/estado_datos.html', locals())