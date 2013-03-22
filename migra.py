# -*- encoding: UTF-8 -*-
from FichaFamilia import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
import csv


def extraer_centros():

    CentroFamiliar.objects.all().delete()

    idcentro_list = []
    centro_obj_list = []
    count = 0

    with open('databackup/DatosFF.csv', 'rb') as datos_familias:
        familia_reader = csv.reader(datos_familias, delimiter=';', quotechar='"')
        for fila in familia_reader:
            idcentrofamiliar = fila[13]
            nombrecentro = fila[14]
            if count < 30:
                if idcentrofamiliar not in idcentro_list:
                    idcentro_list.append(idcentrofamiliar)
                    centro_obj_list.append(
                        CentroFamiliar(id=idcentrofamiliar, comuna=nombrecentro)
                    )
                    count += 1
                    print "%s - %s" % (idcentrofamiliar, nombrecentro)
            else:
                break

    CentroFamiliar.objects.bulk_create(centro_obj_list)

    print CentroFamiliar.objects.all()


def extraer_familias():

    Familia.objects.all().delete()
    familia_obj_list = []
    id_list = []

    with open('databackup/DatosFF.csv', 'rb') as datos_familias:
        familia_reader = csv.reader(datos_familias, delimiter=';', quotechar='"')
        for fila in familia_reader:
            the_id = fila[26]
            if the_id not in id_list:
                id_list.append(the_id)
                familia = Familia()
                familia.id = the_id
                familia.apellido_materno = fila[32]
                familia.apellido_paterno = fila[31]
                familia.numero_integrantes = fila[37]
                familia.ingreso_total_familiar = fila[35]
                familia.tipo_de_familia = fila[33]
                familia.centro_familiar = CentroFamiliar.objects.get(id=fila[13])
                familia_obj_list.append(familia)

    Familia.objects.bulk_create(familia_obj_list)

    print Familia.objects.all().count()


def extraer_columnas_id_descripcion(index_id, index_descripcion, max_distinct_items=100):
    id_list = []
    desc_list = []
    count = 0
    with open('databackup/DatosFF.csv', 'rb') as datos_familias:
        familia_reader = csv.reader(datos_familias, delimiter=';', quotechar='"')
        for fila in familia_reader:
            the_id = fila[index_id]
            nombre = fila[index_descripcion]
            if count < max_distinct_items:
                if the_id not in id_list:
                    id_list.append(the_id)
                    desc_list.append(nombre)
                    count += 1
                    print "    (%s, '%s')," % (the_id, nombre)
            else:
                break

    print ""
    print "Total: %s" % len(id_list)


# centros familiares
extraer_centros()

# estados civiles
#extraer_columnas_id_descripcion(15, 16)

# nivel escolar
#extraer_columnas_id_descripcion(17, 18)

# prevision salud
#extraer_columnas_id_descripcion(19, 20)

# parentesco
#extraer_columnas_id_descripcion(24, 25)

#extraer_columnas_id_descripcion(26, 27, 100000)

# tipo familia
#extraer_columnas_id_descripcion(33, 34)

# ingreso total
#extraer_columnas_id_descripcion(35, 36)

extraer_familias()
  