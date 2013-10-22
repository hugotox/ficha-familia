# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

cursor = connection.cursor()
sql = '''
    ALTER TABLE public.main_familia ADD porcentaje_datos_parte1 double precision NULL;
    --ALTER TABLE public.main_estadofamiliaanio ADD porcentaje_datos_parte2 double precision NULL;
    --ALTER TABLE public.main_estadofamiliaanio ADD porcentaje_datos_parte3 double precision NULL;
    '''
cursor.execute(sql)
transaction.commit_unless_managed()

EstadoFamiliaAnio.objects.all().delete()

for familia in Familia.objects.all():
    familia.actualizar_estado(2013)
    familia.save()

for ev in EvaluacionFactoresProtectores.objects.all():
    ev.save()

# actualiza sexo
Persona.objects.filter(sexo='Masculino').update(sexo='M')
Persona.objects.filter(sexo='Femenino').update(sexo='F')

print "All done"
