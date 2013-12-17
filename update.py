# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

cursor = connection.cursor()
sql = '''
    CREATE TABLE "main_estadocentroanio" (
        "id" serial NOT NULL PRIMARY KEY,
        "centro_id" integer NOT NULL REFERENCES "main_centrofamiliar" ("id") DEFERRABLE INITIALLY DEFERRED,
        "anio" integer NOT NULL,
        "porc_completo_parteI" double precision NOT NULL,
        "porc_completo_parteII_ini" double precision NOT NULL,
        "porc_completo_parteII_cum" double precision NOT NULL,
        "porc_completo_parteIII" double precision NOT NULL,
        UNIQUE ("centro_id", "anio")
    );
    CREATE INDEX "main_estadocentroanio_centro_id" ON "main_estadocentroanio" ("centro_id");
'''
# cursor.execute(sql)
# transaction.commit_unless_managed()


anio = 2013

for centro in CentroFamiliar.objects.all():

    centro.save(anio=anio)

print "All done"
