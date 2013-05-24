# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

# 1. crear columna direccion
try:
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE main_familia ADD COLUMN direccion character varying(250);")
    transaction.commit_unless_managed()
except:
    pass
    
# 2. crear columna ciclo_cerrado
try:
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE main_evaluacionfactoresprotectores ADD COLUMN ciclo_cerrado boolean;")
    transaction.commit_unless_managed()
except:
    pass

# actualizar columna direccion
for fam in Familia.objects.all():
    for per in fam.persona_set.all():
        if per.direccion is not None and per.direccion != '':
            fam.direccion = per.direccion
            fam.save()
            break

print "All done"