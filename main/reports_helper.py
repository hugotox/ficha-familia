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


def get_fichas_por_objetivo(anio):
    sql = '''
        select
          F.id as factor_id,
          count(E.id) as count_eval,
          C.nombre,
          F.objetivo_personal
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
          inner join main_componentes C on F.componente_id = C.id
        WHERE
          E.anio_aplicacion = %s
        group by
          C.id,
          C.nombre,
          F.id,
          F.objetivo_personal
        order by
          C.id,
          F.id;
      '''
    datos = get_dictfetchall_sql(sql, [anio,])

    # fichas activas
    sql = '''
        select
          F.id as factor_id,
          count(E.id) as count_eval
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
        WHERE
          E.anio_aplicacion = %s
          and (E.ciclo_cerrado = false or E.ciclo_cerrado is null)
        group by
          F.id
        order by
          F.id;
      '''
    fichas_activas = get_dictfetchall_sql(sql, [anio, ])

    # fichas completas
    sql = '''
        select
          F.id as factor_id,
          count(E.id) as count_eval
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
        WHERE
          E.anio_aplicacion = %s
          and E.ciclo_cerrado = true
        group by
          F.id
        order by
          F.id;
        '''
    fichas_completas = get_dictfetchall_sql(sql, [anio, ])

    for dato in fichas_activas:
        dato_factor_id = dato['factor_id']
        count_eval = dato['count_eval']

        for datomain in datos:
            if datomain['factor_id'] == dato_factor_id:
                datomain['count_eval_activas'] = count_eval
                break

    for dato in fichas_completas:
        dato_factor_id = dato['factor_id']
        count_eval = dato['count_eval']

        for datomain in datos:
            if datomain['factor_id'] == dato_factor_id:
                datomain['count_eval_completas'] = count_eval
                break

    return datos


def get_fichas_por_objetivo_comuna(anio, factor_id):
    sql = '''
        select
          CF.comuna,
          F.id as factor_id,
          count(E.id) as count_eval
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
          inner join main_componentes C on F.componente_id = C.id
          inner join main_persona P on E.persona_id = P.id
          inner join main_familia FA on P.familia_id = FA.id
          inner join main_centrofamiliar CF on FA.centro_familiar_id = CF.id
        WHERE
          E.anio_aplicacion = %s
          and F.id = %s
        group by
          CF.id,
          CF.comuna,
          C.id,
          F.id
        order by
          CF.comuna,
          C.id,
          F.id;
      '''
    datos = get_dictfetchall_sql(sql, [anio, factor_id])

    # fichas activas
    sql = '''
        select
          CF.comuna,
          F.id as factor_id,
          count(E.id) as count_eval
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
          inner join main_componentes C on F.componente_id = C.id
          inner join main_persona P on E.persona_id = P.id
          inner join main_familia FA on P.familia_id = FA.id
          inner join main_centrofamiliar CF on FA.centro_familiar_id = CF.id
        WHERE
          E.anio_aplicacion = %s
          and (E.ciclo_cerrado = false or E.ciclo_cerrado is null)
          and F.id = %s
        group by
          CF.id,
          CF.comuna,
          C.id,
          F.id
        order by
          CF.comuna,
          C.id,
          F.id
      '''
    fichas_activas = get_dictfetchall_sql(sql, [anio, factor_id])

    # fichas completas
    sql = '''
        select
          CF.comuna,
          F.id as factor_id,
          count(E.id) as count_eval
        from
          main_evaluacionfactoresprotectores E
          inner join main_objetivosevaluacion O on O.evaluacion_id = E.id
          inner join main_factorprotector F on O.factor_id = F.id
          inner join main_componentes C on F.componente_id = C.id
          inner join main_persona P on E.persona_id = P.id
          inner join main_familia FA on P.familia_id = FA.id
          inner join main_centrofamiliar CF on FA.centro_familiar_id = CF.id
        WHERE
          E.anio_aplicacion = %s
          and E.ciclo_cerrado = true
          and F.id = %s
        group by
          CF.id,
          CF.comuna,
          C.id,
          F.id
        order by
          CF.comuna,
          C.id,
          F.id
        '''
    fichas_completas = get_dictfetchall_sql(sql, [anio, factor_id])

    for dato in fichas_activas:
        comuna = dato['comuna']
        count_eval = dato['count_eval']

        for datomain in datos:
            if datomain['comuna'] == comuna:
                datomain['count_eval_activas'] = count_eval
                break

    for dato in fichas_completas:
        comuna = dato['comuna']
        count_eval = dato['count_eval']

        for datomain in datos:
            if datomain['comuna'] == comuna:
                datomain['count_eval_completas'] = count_eval
                break

    return datos


def get_count_condiciones_vulnerabilidad(condicion, valor, id_centro=None):
    """
    condicion: nombre de la columna de la condicion de vulnerabilidad
    valor: debe ser "true|false|null"
    agrupar_por_centro: booleano
    """
    if id_centro:
        sql = """
            select
              c.id,
              c.comuna,
              count(f.id)
            from main_familia f
              inner join main_centrofamiliar c on f.centro_familiar_id = c.id
            where
              f.%s is %s
              and c.id = %s
            group by
              c.id,
              c.comuna
            order by
              c.comuna;
        """ % (condicion, valor, id_centro)
    else:
        sql = """
            select
              count(f.id)
            from main_familia f
            where
              f.%s is %s;
        """ % (condicion, valor)

    return get_dictfetchall_sql(sql)


def get_participacion_actividades(anio):
    actividades = [
        'tall_for_ori',
        'tall_dep_rec',
        'tall_fut_cal',
        'tall_boccias',
        'tall_art_cul',
        'tall_ali_sal',
        'tall_hue_fam',
        'enc_familiar',
        'even_recreat',
        'even_enc_cam',
        'even_dep_fam',
        'even_cultura',
        'mues_fam_art',
        'enc_vida_sal',
        'mod_form_fam',
        'acc_inf_difu',
        'aten_ind_fam',
        'mod_clin_dep',
        'acc_pase_vis',
        'mod_clin_art',
        'acc_recu_are',
        'mod_clin_ali',
    ]

    datos_reporte = get_dictfetchall_sql("select comuna from main_centrofamiliar where comuna <> 'Casa Central' order by comuna;")
    totales = []

    for actividad in actividades:
        sql = '''
            select
              C.comuna,
              count(%s)
            from
              main_evaluacionfactoresprotectores EV
              INNER JOIN (SELECT
                          o.evaluacion_id
                        FROM main_objetivosevaluacion o
                        GROUP BY o.evaluacion_id) AS obj
              ON obj.evaluacion_id = EV.id
              inner join main_persona P on EV.persona_id = P.id
              inner join main_familia F on P.familia_id = F.id
              inner join main_centrofamiliar C on F.centro_familiar_id = C.id
            where
              EV.anio_aplicacion = %s
              and %s = true
              and C.comuna <> 'Casa Central'
            group by
              C.comuna
            order by
              C.comuna
        ''' % (actividad, anio, actividad)
        datos = get_dictfetchall_sql(sql)

        total_act = 0

        for dato in datos:

            comuna = dato['comuna']
            count = dato['count']
            total_act += count

            for dato_rep in datos_reporte:
                if dato_rep['comuna'] == comuna:
                    dato_rep.update({actividad: count})
                    break

        totales.append({
            "actividad": actividad,
            "total": total_act
        })

    return datos_reporte, totales


def get_participacion_actividades_por_objetivo(anio):
    actividades = [
        'tall_for_ori',
        'tall_dep_rec',
        'tall_fut_cal',
        'tall_boccias',
        'tall_art_cul',
        'tall_ali_sal',
        'tall_hue_fam',
        'enc_familiar',
        'even_recreat',
        'even_enc_cam',
        'even_dep_fam',
        'even_cultura',
        'mues_fam_art',
        'enc_vida_sal',
        'mod_form_fam',
        'acc_inf_difu',
        'aten_ind_fam',
        'mod_clin_dep',
        'acc_pase_vis',
        'mod_clin_art',
        'acc_recu_are',
        'mod_clin_ali',
    ]

    datos_reporte = get_dictfetchall_sql("select objetivo_personal from main_factorprotector order by componente_id, id;")

    for actividad in actividades:
        sql = '''
            SELECT
              f.objetivo_personal,
              count(e.%s)
            FROM main_objetivosevaluacion o
              inner join main_factorprotector f on o.factor_id = f.id
              inner join main_evaluacionfactoresprotectores e on o.evaluacion_id = e.id
            where
              e.anio_aplicacion = %s
              and e.%s = true
            GROUP BY
              f.objetivo_personal,
              f.componente_id,
              f.id
            order by
              f.componente_id, f.id;
        ''' % (actividad, anio, actividad)

        datos = get_dictfetchall_sql(sql)

        for dato in datos:

            obj = dato['objetivo_personal']
            count = dato['count']

            for dato_rep in datos_reporte:
                if dato_rep['objetivo_personal'] == obj:
                    dato_rep.update({actividad: count})
                    break

    return datos_reporte


def resultados_por_factor(anio, id_centro=None):

    factores = [
        # relaciones comunitarias
        ("presencia_red_de_apoyo", "Presencia red de apoyo"),
        ("relaciones_con_vecindario", "Relaciones con vecindario"),
        ("participacion_social", "Participación social"),
        # acceso
        ("red_de_servicios_y_beneficios_sociales", "Red de servicios y beneficios sociales"),
        ("ocio_y_encuentro_con_pares", "Ocio y encuentro con pares"),
        ("espacios_formativos_y_de_desarrollo", "Espacios formativos y de desarrollo"),
        # vinculos familiares
        ("relaciones_y_cohesion_familiar", "Relaciones y cohesión familiar"),
        ("adaptabilidad_y_resistencia_familiar", "Adaptabilidad y resiliencia familiar"),
        ("competencias_parentales", "Competencias parentales"),
        # derechos infantiles
        ("proteccion_y_salud_integral", "Protección y salud integral"),
        ("participacion_protagonica", "Participación protagónica"),
        ("recreacion_y_juego_con_pares", "Recreación y juego con pares"),
        # desarrollo personal
        ("crecimiento_personal", "Crecimiento personal"),
        ("autonomia", "Autonomía"),
        ("habilidades_y_valores_sociales", "Habilidades y valores sociales"),
    ]

    componentes = [
        'Desarrollo Personal',
        'Derechos Infantiles',
        u'Vínculos Familiares',
        'Acceso',
        'Relaciones Comunitarias',
    ]

    datos = []
    datos_com = []
    x = 1
    suma_ini = 0.0
    suma_cum = 0.0

    for factor in factores:
        # --- 1. Acceso a la DB
        sql_ini = '''
            select
              avg(e.%s)
            from main_evaluacionfactoresprotectores e
              inner join main_persona p on e.persona_id = p.id
              inner join main_familia f on p.familia_id = f.id
            where e.ciclo_cerrado = true
              and e.anio_aplicacion = %s
              and e.%s <> -100 ''' % (factor[0], anio, factor[0])

        if id_centro is not None:
            sql_ini += " and f.centro_familiar_id = %s" % id_centro

        result_ini = get_dictfetchall_sql(sql_ini)

        factor_cum = factor[0] + "2"

        sql_cum = '''
            select
              avg(e.%s)
            from main_evaluacionfactoresprotectores e
              inner join main_persona p on e.persona_id = p.id
              inner join main_familia f on p.familia_id = f.id
            where e.ciclo_cerrado = true
              and e.anio_aplicacion = %s
              and e.%s <> -100 ''' % (factor_cum, anio, factor_cum)

        if id_centro is not None:
            sql_cum += " and f.centro_familiar_id = %s" % id_centro

        result_cum = get_dictfetchall_sql(sql_cum)

        # ---

        # --- 2. Calculos

        prom_ini = round(result_ini[0]['avg'] or 0, 4)
        prom_cum = round(result_cum[0]['avg'] or 0, 4)

        suma_ini += float( result_ini[0]['avg'] or 0.0 )
        suma_cum += float( result_cum[0]['avg'] or 0.0 )

        if x % 3 == 0:

            datos_com.append({
                'componente': componentes.pop(),
                "ini": round(suma_ini / 3.0, 4),
                "cum": round(suma_cum / 3.0, 4),
                "var": round((suma_cum / 3.0) - (suma_ini / 3.0), 4)
            })
            suma_ini = 0.0
            suma_cum = 0.0

        x += 1

        datos.append({
            "factor": factor[1],
            "prom_ini": prom_ini,
            "prom_cum": prom_cum,
            "var": round(prom_cum - prom_ini, 4)
        })

    return datos, datos_com


def resultados_por_objetivo(anio, centro_id=None):

    mapeo = (
        (u'Promover la presencia de red de apoyo', 'presencia_red_de_apoyo'),
        (u'Promover las relaciones con el vecindario', 'relaciones_con_vecindario'),
        (u'Fomentar la participación social', 'participacion_social'),
        (u'Promover el acceso a la red de servicios y beneficios sociales', 'red_de_servicios_y_beneficios_sociales'),
        (u'Facilitar el acceso a espacios de canalización de ocio y encuentro con pares', 'ocio_y_encuentro_con_pares'),
        (u'Promover el acceso a espacios formativos y de desarrollo', 'espacios_formativos_y_de_desarrollo'),
        (u'Promover las relaciones y cohesión familiar', 'relaciones_y_cohesion_familiar'),
        (u'Facilitar procesos de adaptabilidad y resiliencia familiar', 'adaptabilidad_y_resistencia_familiar'),
        (u'Promover el desarrollo de competencias parentales', 'competencias_parentales'),
        (u'Activar instancias de protección y salud integral', 'proteccion_y_salud_integral'),
        (u'Fomentar la participación protagónica', 'participacion_protagonica'),
        (u'Promover instancias de recreación y juego con pares', 'recreacion_y_juego_con_pares'),
        (u'Promover el crecimiento personal', 'crecimiento_personal'),
        (u'Facilitar el desarrollo de autonomía', 'autonomia'),
        (u'Promover el desarrollo de habilidades y valores sociales', 'habilidades_y_valores_sociales'),
    )

    datos = []

    for m in mapeo:
        sql = '''
            select
              avg(eva.%s) as ini
            from main_evaluacionfactoresprotectores eva
            INNER JOIN main_objetivosevaluacion obj ON obj.evaluacion_id = eva.id
            inner join main_factorprotector fac on obj.factor_id = fac.id
            inner join main_persona per on eva.persona_id = per.id
            inner join main_familia fam on per.familia_id = fam.id
            where eva.ciclo_cerrado = true
              and eva.anio_aplicacion = %s
              and eva.%s <> -100
              and fac.objetivo_personal = '%s'
        ''' % (m[1], anio, m[1], m[0])

        if centro_id is not None:
            sql += ' and fam.centro_familiar_id = %s ' % centro_id

        res = get_dictfetchall_sql(sql)

        col_cum = m[1] + '2'

        sql_cum = '''
            select
              avg(eva.%s) as cum
            from main_evaluacionfactoresprotectores eva
            INNER JOIN main_objetivosevaluacion obj ON obj.evaluacion_id = eva.id
            inner join main_factorprotector fac on obj.factor_id = fac.id
            inner join main_persona per on eva.persona_id = per.id
            inner join main_familia fam on per.familia_id = fam.id
            where eva.ciclo_cerrado = true
              and eva.anio_aplicacion = %s
              and eva.%s <> -100
              and fac.objetivo_personal = '%s'
        ''' % (col_cum, anio, col_cum, m[0])

        if centro_id is not None:
            sql_cum += ' and fam.centro_familiar_id = %s ' % centro_id

        res_cum = get_dictfetchall_sql(sql_cum)

        sql_count = '''
            select
              f.objetivo_personal,
              count(o.id)
            from  main_objetivosevaluacion o
              inner join main_factorprotector f on o.factor_id = f.id
              inner join main_evaluacionfactoresprotectores e on o.evaluacion_id = e.id
              inner join main_persona p on e.persona_id = p.id
              inner join main_familia fam on p.familia_id = fam.id
            where
              e.anio_aplicacion = %s
              and e.ciclo_cerrado = true
              and f.objetivo_personal = '%s'
        ''' % (anio, m[0])

        if centro_id is not None:
            sql_count += ' and fam.centro_familiar_id = %s ' % centro_id

        sql_count += ' group by f.objetivo_personal '

        res_count = get_dictfetchall_sql(sql_count)

        datos.append({
            'objetivo': m[0],
            'count': res_count[0]['count'] if len(res_count) else 0,
            'ini': round(float(res[0]['ini'] or 0.0), 4),
            'cum': round(float(res_cum[0]['cum'] or 0.0), 4),
            'var': round(float(res_cum[0]['cum'] or 0.0) - float(res[0]['ini'] or 0.0), 4)
        })

    return datos