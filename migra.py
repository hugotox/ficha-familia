# -*- encoding: UTF-8 -*-
from FichaFamilia import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
import csv
from django.db import connection, transaction


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
            the_id = fila[27]
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


def extraer_personas():

    Persona.objects.all().delete()
    persona_obj_list = []
    id_list = []

    with open('databackup/DatosFF.csv', 'rb') as datos_familias:
        familia_reader = csv.reader(datos_familias, delimiter=';', quotechar='"')
        for fila in familia_reader:
            the_id = fila[0]
            if the_id not in id_list:
                id_list.append(the_id)

                persona = Persona()
                persona.id = fila[0]
                persona.nombres = fila[2]
                persona.apellido_paterno = fila[3]
                persona.apellido_materno = fila[4]
                persona.rut = fila[1]
                persona.fecha_nacimiento = fila[5] if fila[5] != '' else settings.NULL_DATE
                persona.sexo = fila[8]
                persona.direccion = fila[6]
                persona.telefono = fila[21]
                persona.fecha_participa = fila[28] if fila[28] != '' else settings.NULL_DATE
                persona.fecha_ingreso = fila[11] if fila[11] != '' else settings.NULL_DATE
                persona.estado_civil = fila[15]
                persona.nivel_escolaridad = fila[17]
                persona.ocupacion = fila[10]
                persona.prevision_salud = fila[19]
                # persona.aporta_ingreso = fila[]
                # persona.calificacion_laboral = fila[]
                persona.familia = Familia.objects.get(id=fila[26])
                # persona.principal = fila[]
                persona.parentesco = fila[24]

                persona_obj_list.append(persona)

    Persona.objects.bulk_create(persona_obj_list)

    print Persona.objects.all().count()


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


def actualizar_secuencias():
    # select setval('main_familia_id_seq', (select max(id)+1 from main_familia), false)
    cursor = connection.cursor()

    cursor.execute("select setval('main_familia_id_seq', (select max(id)+1 from main_familia), false)")
    transaction.commit_unless_managed()

    cursor.execute("select setval('main_persona_id_seq', (select max(id)+1 from main_persona), false)")
    transaction.commit_unless_managed()


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

#  ocupacion
#extraer_columnas_id_descripcion(10, 10)

# centros familiares
extraer_centros()

extraer_familias()

extraer_personas()

# actualizar secuencias (SOLO PARA POSTGRESQL):
actualizar_secuencias()