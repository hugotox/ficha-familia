from django.db.models import Count
from django.shortcuts import render
from main.models import *
from utils.sql import get_dictfetchall_sql


def home(request):

    count_familias = Familia.objects.select_related()\
        .values('centro_familiar__comuna')\
        .annotate(count=Count('id'))\
        .order_by('centro_familiar')

    sql = """
        select
          c.id,
          c.comuna,
          count(p.id) as count_personas
        from main_familia f
          inner join main_centrofamiliar c on f.centro_familiar_id = c.id
          inner join main_persona p on p.familia_id = f.id
        group by
          c.id,
          c.comuna
        order by c.comuna
        """

    datos = get_dictfetchall_sql(sql)

    for c1 in datos:

        # agregar el conteo de familias
        for c2 in count_familias:
            if c2['centro_familiar__comuna'] == c1['comuna']:
                c1['count_familias'] = c2['count']
                break

        # agregar la cantidad de fichas activas


    return render(request, 'rep_home.html', {'datos': datos})
