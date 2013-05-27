# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

sql1 = '''
ALTER TABLE main_familia ALTER COLUMN cond_precariedad drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_vulnerabilidad drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_hogar_uni_riesgo drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_familia_mono_riesgo drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_alcohol_drogas drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_discapacidad drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_malos_tratos drop not NULL;
ALTER TABLE main_familia ALTER COLUMN cond_socializ_delictual drop not NULL;

update main_familia set cond_alcohol_drogas = null where cond_alcohol_drogas = false;
update main_familia set cond_discapacidad = null where cond_discapacidad = false;
update main_familia set cond_familia_mono_riesgo = null where cond_familia_mono_riesgo = false;
update main_familia set cond_hogar_uni_riesgo = null where cond_hogar_uni_riesgo = false;
update main_familia set cond_malos_tratos = null where cond_malos_tratos = false;
update main_familia set cond_precariedad = null where cond_precariedad = false;
update main_familia set cond_socializ_delictual = null where cond_socializ_delictual = false;
update main_familia set cond_vulnerabilidad = null where cond_vulnerabilidad = false;

'''

sql2 = "ALTER TABLE main_familia ADD COLUMN direccion character varying(250);"
sql3 = "ALTER TABLE main_evaluacionfactoresprotectores ADD COLUMN ciclo_cerrado boolean;"


cursor = connection.cursor()
cursor.execute(sql1)
transaction.commit_unless_managed()

try:
    cursor.execute(sql2)
except Exception, ex:
    connection._rollback()
else:
    transaction.commit_unless_managed()

try:
    cursor.execute(sql3)
except Exception, ex:
    connection._rollback()
else:
    transaction.commit_unless_managed()

# actualizar columna direccion
for fam in Familia.objects.all():
    for per in fam.persona_set.all():
        if per.direccion is not None and per.direccion != '':
            fam.direccion = per.direccion
            fam.save()
            break

print "All done"