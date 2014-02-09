# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

cursor = connection.cursor()
sql = """
alter table main_estadofamiliaanio add "cond_precariedad" boolean;
alter table main_estadofamiliaanio add "cond_precariedad_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_vulnerabilidad" boolean;
alter table main_estadofamiliaanio add "cond_vulnerabilidad_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_hogar_uni_riesgo" boolean;
alter table main_estadofamiliaanio add "cond_hogar_uni_riesgo_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_familia_mono_riesgo" boolean;
alter table main_estadofamiliaanio add "cond_familia_mono_riesgo_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_alcohol_drogas" boolean;
alter table main_estadofamiliaanio add "cond_alcohol_drogas_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_discapacidad" boolean;
alter table main_estadofamiliaanio add "cond_discapacidad_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_malos_tratos" boolean;
alter table main_estadofamiliaanio add "cond_malos_tratos_coment" varchar(250);
alter table main_estadofamiliaanio add "cond_socializ_delictual" boolean;
alter table main_estadofamiliaanio add "cond_socializ_delictual_coment" varchar(250);
"""
cursor.execute(sql)
transaction.commit_unless_managed()

for familia in Familia.objects.all():
    estado, created = EstadoFamiliaAnio.objects.get_or_create(familia=familia, anio=2013)
    estado.cond_precariedad = familia.cond_precariedad
    estado.cond_precariedad_coment = familia.cond_precariedad_coment
    estado.cond_vulnerabilidad = familia.cond_vulnerabilidad
    estado.cond_vulnerabilidad_coment = familia.cond_vulnerabilidad_coment
    estado.cond_hogar_uni_riesgo = familia.cond_hogar_uni_riesgo
    estado.cond_hogar_uni_riesgo_coment = familia.cond_hogar_uni_riesgo_coment
    estado.cond_familia_mono_riesgo = familia.cond_familia_mono_riesgo
    estado.cond_familia_mono_riesgo_coment = familia.cond_familia_mono_riesgo_coment
    estado.cond_alcohol_drogas = familia.cond_alcohol_drogas
    estado.cond_alcohol_drogas_coment = familia.cond_alcohol_drogas_coment
    estado.cond_discapacidad = familia.cond_discapacidad
    estado.cond_discapacidad_coment = familia.cond_discapacidad_coment
    estado.cond_malos_tratos = familia.cond_malos_tratos
    estado.cond_malos_tratos_coment = familia.cond_malos_tratos_coment
    estado.cond_socializ_delictual = familia.cond_socializ_delictual
    estado.cond_socializ_delictual_coment = familia.cond_socializ_delictual_coment
    estado.save()
print "All done"
