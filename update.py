# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

# cursor = connection.cursor()
# sql = '''
#    update main_familia set porcentaje_datos_parte1=null;
# '''
# cursor.execute(sql)
# transaction.commit_unless_managed()

print "Actualizando familias..."

familia_qs = Familia.objects.all()

for familia in familia_qs:
    familia.save()  # actualiza datos parte 1

print "Actualizando evaluaciones..."

evals_qs = EvaluacionFactoresProtectores.objects.all()

for ev in evals_qs:
    ev.save()

print "All done"
