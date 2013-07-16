from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.reports_helper import get_familias_por_centro, get_personas_por_centro, get_fichas_activas_por_centro
from utils.json_utils import json_response


@login_required
def home(request, anio):

    active = 'cobertura'

    # conteo de familias por centro
    count_familias = get_familias_por_centro()

    # conteo de personas por centro
    datos = get_personas_por_centro()

    # conteo de fichas activas
    fichas_activas = get_fichas_activas_por_centro(anio)

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

    return render(request, 'reportes/cobertura.html', locals())


@login_required
def cobertura(request, anio, tipo):
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
                'text': 'Cobertura'
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

        fichas_activas = get_fichas_activas_por_centro(anio)

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
    return render(request, "reportes/tipos_familias.html", locals())