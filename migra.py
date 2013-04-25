# -*- encoding: UTF-8 -*-
from FichaFamilia import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
import csv
from django.db import connection, transaction
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


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
                persona.fecha_nacimiento = fila[5].split(" ")[0] if fila[5] != '' else settings.NULL_DATE
                persona.sexo = fila[8]
                persona.direccion = fila[6]
                persona.telefono = fila[21]
                persona.fecha_participa = fila[28].split(" ")[0] if fila[28] != '' else settings.NULL_DATE
                persona.fecha_ingreso = fila[11].split(" ")[0] if fila[11] != '' else settings.NULL_DATE
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

    cursor.execute("select setval('main_centrofamiliar_id_seq', (select max(id)+1 from main_centrofamiliar), false)")
    transaction.commit_unless_managed()

    cursor.execute("select setval('main_familia_id_seq', (select max(id)+1 from main_familia), false)")
    transaction.commit_unless_managed()

    cursor.execute("select setval('main_persona_id_seq', (select max(id)+1 from main_persona), false)")
    transaction.commit_unless_managed()


def crear_componentes_y_objetivos():

    FactorProtector.objects.all().delete()
    Componentes.objects.all().delete()

    comp = Componentes.objects.create(nombre="Relaciones Comunitarias")
    FactorProtector.objects.create(componente=comp, factor_protector="Presencia red de apoyo", objetivo_personal="Promover la presencia de red de apoyo")
    FactorProtector.objects.create(componente=comp, factor_protector="Relaciones con vecindario", objetivo_personal="Promover las relaciones con el vecindario")
    FactorProtector.objects.create(componente=comp, factor_protector="Participación social", objetivo_personal="Fomentar la participación social")

    comp = Componentes.objects.create(nombre="Acceso")
    FactorProtector.objects.create(componente=comp, factor_protector="Red de servicios y beneficios sociales",
                                   objetivo_personal="Promover el acceso a la red de servicios y beneficios sociales",
                                   objetivo_grupal="Promover el acceso a la red de servicios y beneficios sociales")
    FactorProtector.objects.create(componente=comp, factor_protector="Ocio y encuentro con pares",
                                   objetivo_personal="Facilitar el acceso a espacios de canalización de ocio y encuentro con pares")
    FactorProtector.objects.create(componente=comp, factor_protector="Espacios formativos y de desarrollo",
                                   objetivo_personal="Promover el acceso a espacios formativos y de desarrollo")

    comp = Componentes.objects.create(nombre="Vínculos Familiares")
    FactorProtector.objects.create(componente=comp, factor_protector="Relaciones y cohesión familiar",
                                   objetivo_personal="Promover las relaciones y cohesión familiar",
                                   objetivo_grupal="Promover las relaciones y cohesión familiar")
    FactorProtector.objects.create(componente=comp, factor_protector="Adaptabilidad y resistencia familiar",
                                   objetivo_personal="Facilitar procesos de adaptabilidad y resiliencia familiar",
                                   objetivo_grupal="Facilitar procesos de adaptabilidad y resiliencia familiar")
    FactorProtector.objects.create(componente=comp, factor_protector="Competencias parentales",
                                   objetivo_personal="Promover el desarrollo de competencias parentales")

    comp = Componentes.objects.create(nombre="Derechos Infantiles")
    FactorProtector.objects.create(componente=comp, factor_protector="Protección y salud integral", objetivo_personal="Activar instancias de protección y salud integral")
    FactorProtector.objects.create(componente=comp, factor_protector="Participación protagónica", objetivo_personal="Fomentar la participación protagónica")
    FactorProtector.objects.create(componente=comp, factor_protector="Recreación y juego con pares", objetivo_personal="Promover instancias de recreación y juego con pares")

    comp = Componentes.objects.create(nombre="Desarrollo Personal")
    FactorProtector.objects.create(componente=comp, factor_protector="Crecimiento personal ", objetivo_personal="Promover el crecimiento personal")
    FactorProtector.objects.create(componente=comp, factor_protector="Autonomía ", objetivo_personal="Facilitar el desarrollo de autonomía")
    FactorProtector.objects.create(componente=comp, factor_protector="Habilidades y valores sociales ", objetivo_personal="Promover el desarrollo de habilidades y valores sociales")


def crear_usuarios():
    User.objects.exclude(username="admin").delete()

    master_pass = "fun_familia2013"

    centros = [
        ('antofagasta', 'Antofagasta'),
        ('copiapo', 'Copiapo'),
        ('coquimbo', 'Coquimbo'),
        ('curico', 'Curico'),
        ('talca', 'Talca'),
        ('talcahuano', 'Talcahuano'),
        ('temuco', 'Temuco'),
        ('puertomontt', 'Puerto Montt'),
        ('penalolen', 'Recoleta'),
        ('recoleta', u'Peñalolen'),
        ('lapintana', 'La Florida'),
        ('laflorida', 'La Pintana'),
        ('sanbernardo', 'San Bernardo'),
    ]

    for tupla_centro in centros:
        comuna = tupla_centro[1]
        nom_user = tupla_centro[0]
        usuarios = [nom_user, "%s2" % nom_user, "ac%s" % nom_user, "ac%s2" % nom_user]
        centro = CentroFamiliar.objects.get(comuna=comuna)

        for nombre_usuario in usuarios:
            user = User.objects.create_user(nombre_usuario, '', master_pass)
            UserProfile.objects.create(user=user, centro_familiar=centro)
            print "Creado %s" % nombre_usuario

    # Usuarios casa central
    casa_central = CentroFamiliar.objects.create(comuna="Casa Central")

    user = User.objects.create_superuser('apastore', '', master_pass)
    UserProfile.objects.create(user=user, centro_familiar=casa_central)

    user = User.objects.create_superuser('craby', '', master_pass)
    UserProfile.objects.create(user=user, centro_familiar=casa_central)

    user = User.objects.create_superuser('vgutierrez', '', master_pass)
    UserProfile.objects.create(user=user, centro_familiar=casa_central)


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

if True:
    extraer_centros()

    extraer_familias()

    extraer_personas()

    # actualizar secuencias (SOLO PARA POSTGRESQL):
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        actualizar_secuencias()

    crear_componentes_y_objetivos()
    crear_usuarios()
