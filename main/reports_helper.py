# -*- encoding: UTF-8 -*-
from django.db.models import Count
from main.models import Familia
from utils.sql import get_dictfetchall_sql


def get_familias_por_centro():
    count_familias = Familia.objects.select_related()\
        .exclude(centro_familiar__comuna='Casa Central')\
        .values('centro_familiar__comuna')\
        .annotate(count=Count('id'))\
        .order_by('centro_familiar__comuna')
    return count_familias


def get_personas_por_centro():
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
    return datos


def get_conteo_fichas_por_centro(anio, estado='activas'):

    if estado not in ['activas', 'cerradas']:
        estado = 'activas'

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
                            e.anio_aplicacion = %s """

    if estado == 'activas':
        sql += """ and (e.ciclo_cerrado is null or e.ciclo_cerrado is false) """
    else:
        sql += """ and (e.ciclo_cerrado is true) """

    sql += """
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
    return fichas_activas


def get_conteo_familias_por_tipo(anio, centro, solo_activas):

    sql_select = u"""
        select
          c.comuna,
          f.tipo_de_familia,
          case
            when f.tipo_de_familia=1 then 'Monoparental Madre'
            when f.tipo_de_familia=2 then 'Monoparental Padre'
            when f.tipo_de_familia=3 then 'Monoparental Abuelo/a'
            when f.tipo_de_familia=4 then 'Monoparental Otro Adulto Responsable'
            when f.tipo_de_familia=5 then 'Nuclear Simple (sin hijos)'
            when f.tipo_de_familia=6 then 'Nuclear Biparental (con hijos)'
            when f.tipo_de_familia=7 then 'Extendida'
            when f.tipo_de_familia=8 then 'Otras'
            else 'Sin Información'
          end as tipo,
          count(f.id)
        from main_familia f
          inner join main_centrofamiliar c on f.centro_familiar_id=c.id
    """
    sql_params = [centro]

    sql_where = u"""
        where
          c.comuna = %s
    """
    if solo_activas:
        sql_where += u"""
            """

    sql_group_by = u"""
        group by
            c.comuna,
            f.tipo_de_familia,
            tipo
          order by c.comuna, f.tipo_de_familia;
    """

    return get_dictfetchall_sql(sql_select + sql_where + sql_group_by, sql_params)


def get_relacion_familia_ficha(anio):
    sql = '''
    select
      tabla_per.cid,
      C.comuna,
      tabla_per.cant_personas,
      --tabla_act.actividad
      round(tabla_act.actividad * 100 / tabla_per.cant_personas, 2) as porcentaje
      from (
        select
          T.cid,
          round( avg(T.count_persona), 2 ) as actividad
        from(
          select
            F.centro_familiar_id as cid,
            F.id as fid,
            count(P.id) as count_persona
          from main_familia F
            inner join main_persona P on P.familia_id = F.id
            inner join main_evaluacionfactoresprotectores E on E.persona_id = P.id
            INNER JOIN (SELECT
                          o.evaluacion_id
                        FROM main_objetivosevaluacion o
                        GROUP BY o.evaluacion_id) AS obj
              ON obj.evaluacion_id = E.id
          where
            E.anio_aplicacion=%s
          group by
            cid,
            fid
          order by
            cid
           ) as T
        group by
          cid
      ) as tabla_act

      inner join (
         select
          T.cid,
          round( avg(T.count_persona), 2 ) as cant_personas
        from(
          select
            F.centro_familiar_id as cid,
            F.id as fid,
            count(P.id) as count_persona
          from main_familia F
            inner join main_persona P on P.familia_id = F.id
          where
            true
          group by
            cid,
            fid
          order by
            cid) as T
        group by
          cid
        ) as tabla_per

      on tabla_per.cid = tabla_act.cid

      inner join main_centrofamiliar as C on tabla_per.cid = C.id

      order by C.comuna
        '''

    return get_dictfetchall_sql(sql, [anio,])