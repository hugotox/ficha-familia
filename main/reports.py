from django.db.models import Count
from django.shortcuts import render
from main.models import *
from utils.json_utils import JSONEncoderX, json_response
from utils.sql import get_dictfetchall_sql
from datetime import date
from django.utils import simplejson


def home(request, anio):

    # conteo de familias por centro
    count_familias = Familia.objects.select_related()\
        .values('centro_familiar__comuna')\
        .annotate(count=Count('id'))\
        .order_by('centro_familiar__comuna')

    # conteo de personas por centro
    sql = """
        select
          c.id,
          c.comuna,
          count(p.id) as count_personas
        from main_familia f
          inner join main_centrofamiliar c on f.centro_familiar_id = c.id
          inner join main_persona p on p.familia_id = f.id
        where
          c.comuna <> 'Casa Central'
        group by
          c.id,
          c.comuna
        order by c.comuna
        """

    datos = get_dictfetchall_sql(sql)

    # conteo de fichas activas
    sql = """
        select
          c.id as comuna_id,
          c.comuna,
          count(p.id) as count_fichas
        from main_centrofamiliar c
          inner join main_familia f on f.centro_familiar_id = c.id
          inner join main_persona p on p.familia_id = f.id
          inner join main_evaluacionfactoresprotectores e on e.persona_id = p.id
          inner join (select o.evaluacion_id from main_objetivosevaluacion o group by o.evaluacion_id) as obj on obj.evaluacion_id = e.id
        where
          e.anio_aplicacion = %s
          and e.ciclo_cerrado = false
          and c.comuna <> 'Casa Central'
        group by
          c.id,
          c.comuna
        order by c.comuna
    """
    fichas_activas = get_dictfetchall_sql(sql, [anio])

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
                'name': 'Total Familias',
                'data': [x['count_familias'] for x in datos]
            }
        ]
    }

    grafico_cobertura_json = simplejson.dumps(grafico_cobertura, cls=JSONEncoderX)

    return render(request, 'rep_home.html', locals())


def cobertura(request, anio, tipo):
    grafico_cobertura = ''

    if tipo == 'familias':
        count_familias = Familia.objects.select_related()\
            .exclude(centro_familiar__comuna='Casa Central')\
            .values('centro_familiar__comuna')\
            .annotate(count=Count('id'))\
            .order_by('centro_familiar__comuna')

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
        sql = """
            select
              c.id,
              c.comuna,
              count(p.id) as count_personas
            from main_familia f
              inner join main_centrofamiliar c on f.centro_familiar_id = c.id
              inner join main_persona p on p.familia_id = f.id
            where
              c.comuna <> 'Casa Central'
            group by
              c.id,
              c.comuna
            order by c.comuna
            """

        datos = get_dictfetchall_sql(sql)

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
        sql = """
            SELECT
              c.id AS comuna_id,
              c.comuna,
              CASE WHEN conteo.count_fichas IS null THEN 0
              ELSE conteo.count_fichas
              END
            FROM main_centrofamiliar c
              LEFT JOIN (
                          SELECT
                            c.id        AS comuna_id,
                            c.comuna,
                            count(p.id) AS count_fichas
                          FROM main_centrofamiliar c
                            INNER JOIN main_familia f
                              ON f.centro_familiar_id = c.id
                            INNER JOIN main_persona p
                              ON p.familia_id = f.id
                            INNER JOIN main_evaluacionfactoresprotectores e
                              ON e.persona_id = p.id
                            INNER JOIN (SELECT
                                          o.evaluacion_id
                                        FROM main_objetivosevaluacion o
                                        GROUP BY o.evaluacion_id) AS obj
                              ON obj.evaluacion_id = e.id
                          WHERE
                            e.anio_aplicacion = %s
                            AND e.ciclo_cerrado = FALSE
                            AND c.comuna <> 'Casa Central'
                          GROUP BY
                            c.id,
                            c.comuna
                          ORDER BY c.comuna
                        ) AS conteo
                ON conteo.comuna_id = c.id
            WHERE c.comuna <> 'Casa Central'
            ORDER BY c.comuna;
        """

        fichas_activas = get_dictfetchall_sql(sql, [anio])

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