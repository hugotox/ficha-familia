# -*- encoding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.db.models import Sum
from django.forms.widgets import DateInput
from datetime import datetime
import settings
from utils.widgets import RutInput, HorizontalRadio

PRESENTE_CHOICES = (
    (True, u'Presente'),
    (False, u'No presente'),
)

NIVEL_ESC_CHOICES = (
    (1, 'Básica'),
    (2, 'Media'),
    (3, 'Universitaria'),
    (4, 'Técnica'),
    (5, 'Básica Incompleta'),
    (6, 'Media Incompleta'),
    (7, 'Técnica Incompleta'),
    (8, 'Universitaria Incompleta'),
    (10, 'Pre-Escolar'),
)

CALIFICACION_LABORAL_CHOICES = (
    (u'Estable', u'Estable'),
    (u'Esporádico', u'Esporádico'),
    (u'Desempleado', u'Desempleado'),
    (u'Independiente Formal', u'Independiente Formal'),
    (u'Independiente Informal', u'Independiente Informal'),
    (u'Otros', u'Otros'),
)

INGRESO_TOTAL_CHOICES = (
    (1, 'Entre 0 y 100.000'),
    (2, 'Entre 100.001 y 200.000'),
    (3, 'Entre 200.001 y 300.000'),
    (4, 'Entre 300.001 y 400.000'),
    (5, 'Entre 400.001 y 500.000'),
    (6, 'Más de 500.000'),
)

TIPOS_FAMILIA_CHOICES = (
    (1, 'Monoparental Madre'),
    (2, 'Monoparental Padre'),
    (3, 'Monoparental Abuelo/a'),
    (4, 'Monoparental Otro Adulto Responsable'),
    (5, 'Nuclear Simple (sin hijos)'),
    (6, 'Nuclear Biparental (con hijos)'),
    (7, 'Extendida'),
    (8, 'Otras'),
)

SEXO_CHOICES = (('M', 'Masculino'), ('F', 'Femenino'))

ESTADO_CIVIL_CHOICES = (
    (1, 'Soltero (a)'),
    (2, 'Casado (a)'),
    (3, 'Viudo (a)'),
    (4, 'Separado (a)'),
    (5, 'Convive'),
)

ETAPA_EVAL_CHOICES = (('inicio', 'Inicio'), ('cumplimiento', 'Cumplimiento'))

OBJS_EVAL_CHOICES = (
    (1, "Individual"),
    (2, "Grupo Familiar"),
)

OCUPACION_CHOICES = (
    u'Dueña de casa',
    u'Empleado',
    u'Comerciante',
    u'Obrero',
    u'Otro',
    u'Estudiante',
)

ESTADO_FAMILIA_CHOICES = (
    ('Inactivo', 'Inactivo'),
    ('Activo', 'Activo'),
    ('Completo', 'Completo')
)

PREVISION_SALUD_CHOICES = (
    (1, 'Isapre'),
    (2, 'INP'),
    (3, 'Fonasa'),
    (4, 'Capredena'),
    (6, 'Sin Previsión'),
)

PARENTESCO_CHOICES = (
    (10, 'Esposo (a)'),
    (1, 'Padre'),
    (2, 'Madre'),
    (3, 'Hijo (a)'),
    (4, 'Hermano (a)'),
    (5, 'Abuelo (a)'),
    (6, 'Nieto (a)'),
    (7, 'Tio (a)'),
    (8, 'Primo (a)'),
    (9, 'Otro'),
)


class CentroFamiliar(models.Model):
    comuna = models.CharField(max_length=250)

    class Meta:
        ordering = ['comuna']

    def __unicode__(self):
        return self.comuna

    def get_porcentaje_completo(self):
        familias = self.familia_set.all()
        cant_familias = familias.count()
        suma = sum([x.porcentaje_datos_parte1 for x in familias])
        return suma / cant_familias

    def get_porcentaje_completo_p2(self, anio):
        familias = self.familia_set.all()
        cant_familias = familias.count()
        datos = familias.select_related('estadofamiliaanio').aggregate(Sum("estadofamiliaanio__porcentaje_datos_parte2"))
        suma = datos['estadofamiliaanio__porcentaje_datos_parte2__sum'] or 0
        return suma / cant_familias

    def get_porcentaje_completo_p3(self):
        familias = self.familia_set.all()
        cant_familias = familias.count()
        datos = familias.select_related('estadofamiliaanio').aggregate(Sum("estadofamiliaanio__porcentaje_datos_parte3"))
        suma = datos['estadofamiliaanio__porcentaje_datos_parte3__sum'] or 0
        return suma / cant_familias


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    centro_familiar = models.ForeignKey(CentroFamiliar, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Familia(models.Model):
    apellido_materno = models.CharField(max_length=250)  # apellidos de la familia
    apellido_paterno = models.CharField(max_length=250)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes', help_text='(que viven en el hogar)', )
    ingreso_total_familiar = models.IntegerField(choices=INGRESO_TOTAL_CHOICES, null=True, blank=True)
    tipo_de_familia = models.IntegerField(choices=TIPOS_FAMILIA_CHOICES, null=True, blank=True)
    direccion = models.CharField(max_length=250, verbose_name=u'Dirección', null=True, blank=True)

    cond_precariedad = models.NullBooleanField(default=None, verbose_name=u'Condiciones de precariedad: vivienda, trabajo, situación sanitaria, otras.', blank=True, null=True)
    cond_precariedad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_vulnerabilidad = models.NullBooleanField(default=None, verbose_name=u'Vulnerabilidad barrial (inseguridad, violencia, estigma, pocos accesos).', blank=True, null=True)
    cond_vulnerabilidad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_hogar_uni_riesgo = models.NullBooleanField(default=None, verbose_name=u'Hogar unipersonal en situación de riesgo.', blank=True, null=True)
    cond_hogar_uni_riesgo_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_familia_mono_riesgo = models.NullBooleanField(default=None, verbose_name=u'Familia monoparental en situación de riesgo.', blank=True, null=True)
    cond_familia_mono_riesgo_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_alcohol_drogas = models.NullBooleanField(default=None, verbose_name=u'Consumo problemático de alcohol y/o drogas.', blank=True, null=True)
    cond_alcohol_drogas_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_discapacidad = models.NullBooleanField(default=None, verbose_name=u'Presencia de discapacidad física y/o mental.', blank=True, null=True)
    cond_discapacidad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_malos_tratos = models.NullBooleanField(default=None, verbose_name=u'Experiencias de malos tratos (actual o histórica).', blank=True, null=True)
    cond_malos_tratos_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_socializ_delictual = models.NullBooleanField(default=None, verbose_name=u'Historial de socialización delictual (detenciones, problemas judiciales).', blank=True, null=True)
    cond_socializ_delictual_coment = models.CharField(max_length=250, null=True, blank=True)

    centro_familiar = models.ForeignKey(CentroFamiliar, null=True, blank=True)

    # deprecado NO USAR!!! Ahora el estado se almacena en la tabla estadofamiliaanio
    estado = models.CharField(max_length=250, null=True, blank=True, choices=ESTADO_FAMILIA_CHOICES, default=ESTADO_FAMILIA_CHOICES[0][0])

    date_created = models.DateTimeField(default=datetime.now())
    date_modified = models.DateTimeField(auto_now=True)

    porcentaje_datos_parte1 = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.apellido_paterno, self.apellido_materno)

    def actualizar_estado(self, anio=None):
        self.get_estado(True, anio)

    def get_estado(self, save_to_db=False, anio=None):
        """
        Estado es activo cuando existe al menos una persona con ficha y esta tiene al menos un objetivo.
        Estado es cerrado cuando existe al menos una ficha cerrada
        Estado es inactivo cuando existe al menos una persona inactiva
        """
        if anio is None:
            anio = datetime.now().year
        personas_qs = self.persona_set.all()

        inactivo = 0
        activo = 0
        cerrado = 0

        for persona in personas_qs:

            evaluacion_qs = persona.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio)

            if evaluacion_qs.count() == 0:
                inactivo += 1
            else:
                for evaluacion in evaluacion_qs:
                    if evaluacion.objetivosevaluacion_set.count() == 0:
                        inactivo += 1
                    else:
                        if evaluacion.ciclo_cerrado:
                            cerrado += 1
                        else:
                            activo += 1

        if save_to_db:
            estado_obj, created = self.estadofamiliaanio_set.get_or_create(anio=anio)
            estado_obj.inactivo = inactivo != 0
            estado_obj.activo = activo != 0
            estado_obj.completo = cerrado != 0
            if estado_obj.porcentaje_datos_parte2 is None:
                estado_obj.porcentaje_datos_parte2 = self.get_porcentaje_completo_p2(anio)
            if estado_obj.porcentaje_datos_parte3 is None:
                estado_obj.porcentaje_datos_parte3 = self.get_porcentaje_completo_p3(anio)
            estado_obj.save()

        return "A: %s, I: %s, C: %s" % (activo, inactivo, cerrado)

    def get_porcentaje_completo(self):
        anio = datetime.now().year
        # obtener solo las personas con ficha activa
        personas_all = self.persona_set.all()
        objetivos = ObjetivosEvaluacion.objects.filter(evaluacion__anio_aplicacion=anio,
                                                       evaluacion__ciclo_cerrado=False,
                                                       evaluacion__persona__in=personas_all)
        personas_list = []
        for obj in objetivos:
            personas_list.append(obj.evaluacion.persona)
        suma = 0
        total_posible = 15 + 14 * len(personas_list)
        if self.apellido_paterno is not None and self.apellido_paterno != '':
            suma += 1
        if self.apellido_materno is not None and self.apellido_materno != '':
            suma += 1
        if self.numero_integrantes is not None:
            suma += 1
        if self.direccion is not None and self.direccion != '':
            suma += 1
        if self.centro_familiar is not None and self.centro_familiar != '':
            suma += 1
        if self.ingreso_total_familiar is not None:
            suma += 1
        if self.tipo_de_familia is not None and self.tipo_de_familia != '':
            suma += 1
        if self.cond_precariedad is not None:
            suma += 1
        if self.cond_vulnerabilidad is not None:
            suma += 1
        if self.cond_hogar_uni_riesgo is not None:
            suma += 1
        if self.cond_familia_mono_riesgo is not None:
            suma += 1
        if self.cond_alcohol_drogas is not None:
            suma += 1
        if self.cond_discapacidad is not None:
            suma += 1
        if self.cond_malos_tratos is not None:
            suma += 1
        if self.cond_socializ_delictual is not None:
            suma += 1

        for per in personas_list:
            if per.nombres is not None and per.nombres != '':
                suma += 1
            if per.apellido_paterno is not None and per.apellido_paterno != '':
                suma += 1
            if per.apellido_materno is not None and per.apellido_materno != '':
                suma += 1
            if per.rut is not None and per.rut != '':
                suma += 1
            if per.fecha_nacimiento is not None and per.fecha_nacimiento != settings.NULL_DATE:
                suma += 1
            if per.sexo is not None and per.sexo != '':
                suma += 1
            if per.telefono is not None and per.telefono != '':
                suma += 1
            if per.fecha_ingreso is not None and per.fecha_ingreso != settings.NULL_DATE:
                suma += 1
            if per.estado_civil is not None and per.estado_civil != '':
                suma += 1
            if per.nivel_escolaridad is not None and per.nivel_escolaridad != '':
                suma += 1
            if per.ocupacion is not None and per.ocupacion != "":
                suma += 1
            if per.prevision_salud is not None and per.prevision_salud != '':
                suma += 1
            if per.aporta_ingreso is not None:
                suma += 1
            if per.parentesco is not None and per.parentesco != '':
                suma += 1

        return 100.0 * suma / total_posible

    def get_porcentaje_completo_p2(self, anio):
        total_posible = 30
        suma = 0
        personas_qs = self.persona_set.all()
        for persona in personas_qs:
            evals = persona.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio, ciclo_cerrado=False)
            if evals.count() > 0:
                ev = evals[0]
                if ev.objetivosevaluacion_set.all().count():  # evaluacion activa

                    if ev.presencia_red_de_apoyo is not None:
                        suma += 1
                    if ev.presencia_red_de_apoyo2 is not None:
                        suma += 1
                    if ev.relaciones_con_vecindario is not None:
                        suma += 1
                    if ev.relaciones_con_vecindario2 is not None:
                        suma += 1
                    if ev.participacion_social is not None:
                        suma += 1
                    if ev.participacion_social2 is not None:
                        suma += 1
                    if ev.red_de_servicios_y_beneficios_sociales is not None:
                        suma += 1
                    if ev.red_de_servicios_y_beneficios_sociales2 is not None:
                        suma += 1
                    if ev.ocio_y_encuentro_con_pares is not None:
                        suma += 1
                    if ev.ocio_y_encuentro_con_pares2 is not None:
                        suma += 1
                    if ev.espacios_formativos_y_de_desarrollo is not None:
                        suma += 1
                    if ev.espacios_formativos_y_de_desarrollo2 is not None:
                        suma += 1
                    if ev.relaciones_y_cohesion_familiar is not None:
                        suma += 1
                    if ev.relaciones_y_cohesion_familiar2 is not None:
                        suma += 1
                    if ev.adaptabilidad_y_resistencia_familiar is not None:
                        suma += 1
                    if ev.adaptabilidad_y_resistencia_familiar2 is not None:
                        suma += 1
                    if ev.competencias_parentales is not None:
                        suma += 1
                    if ev.competencias_parentales2 is not None:
                        suma += 1
                    if ev.proteccion_y_salud_integral is not None:
                        suma += 1
                    if ev.proteccion_y_salud_integral2 is not None:
                        suma += 1
                    if ev.participacion_protagonica is not None:
                        suma += 1
                    if ev.participacion_protagonica2 is not None:
                        suma += 1
                    if ev.recreacion_y_juego_con_pares is not None:
                        suma += 1
                    if ev.recreacion_y_juego_con_pares2 is not None:
                        suma += 1
                    if ev.crecimiento_personal is not None:
                        suma += 1
                    if ev.crecimiento_personal2 is not None:
                        suma += 1
                    if ev.autonomia is not None:
                        suma += 1
                    if ev.autonomia2 is not None:
                        suma += 1
                    if ev.habilidades_y_valores_sociales is not None:
                        suma += 1
                    if ev.habilidades_y_valores_sociales2 is not None:
                        suma += 1

        return 100.0 * suma / total_posible

    def get_porcentaje_completo_p3(self, anio):
        total_posible = 4
        suma = 0
        personas_qs = self.persona_set.all()
        for persona in personas_qs:
            evals = persona.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio, ciclo_cerrado=False)
            if evals.count() > 0:
                ev = evals[0]
                if ev.objetivosevaluacion_set.all().count():  # evaluacion activa
                    suma += 1  # objetivos
                    if ev.propuesta_ciclo_desarrollo_socio_fam is not None and ev.propuesta_ciclo_desarrollo_socio_fam != "":
                        suma += 1

                    act_fila1 = ev.tall_for_ori or ev.tall_dep_rec or ev.tall_fut_cal or ev.tall_boccias \
                        or ev.tall_art_cul or ev.tall_ali_sal or ev.tall_hue_fam

                    act_fila2 = ev.enc_familiar or ev.even_recreat or ev.even_enc_cam or ev.even_dep_fam \
                        or ev.even_cultura or ev.mues_fam_art or ev.enc_vida_sal

                    act_fila3 = ev.mod_form_fam or ev.acc_inf_difu or ev.aten_ind_fam or ev.mod_clin_dep \
                        or ev.acc_pase_vis or ev.mod_clin_art or ev.acc_recu_are or ev.mod_clin_ali

                    act_col1 = ev.tall_for_ori or ev.enc_familiar or ev.even_recreat or ev.mod_form_fam \
                        or ev.acc_inf_difu or ev.aten_ind_fam

                    act_col2 = ev.tall_dep_rec or ev.tall_fut_cal or ev.tall_boccias or ev.tall_art_cul \
                        or ev.tall_ali_sal or ev.tall_hue_fam or ev.even_enc_cam or ev.even_dep_fam \
                        or ev.even_cultura or ev.mues_fam_art or ev.enc_vida_sal or ev.mod_clin_dep \
                        or ev.acc_pase_vis or ev.mod_clin_art or ev.acc_recu_are or ev.mod_clin_ali

                    if act_fila1 and act_fila2 and act_fila3 and act_col1 and act_col2:
                        suma += 1

                    if ev.evaluacion_cualitativa is not None and ev.evaluacion_cualitativa != '':
                        suma += 1

        return 100.0 * suma / total_posible

    def save(self, *args, **kwargs):
        self.porcentaje_datos_parte1 = self.get_porcentaje_completo()
        super(Familia, self).save(*args, **kwargs)


class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellido_paterno = models.CharField(max_length=250)
    apellido_materno = models.CharField(max_length=250)
    rut = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=9, choices=SEXO_CHOICES, null=True, blank=True)

    # deprecado: direccion pertenece a familia
    direccion = models.CharField(max_length=250, verbose_name=u'Dirección', null=True, blank=True)
    telefono = models.CharField(max_length=250, verbose_name=u'Teléfono de contacto', null=True, blank=True)
    fecha_participa = models.DateField(verbose_name='Desde cuándo participa en FF', null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)

    estado_civil = models.IntegerField(null=True, blank=True, choices=ESTADO_CIVIL_CHOICES, default=0)
    nivel_escolaridad = models.IntegerField(null=True, blank=True, choices=NIVEL_ESC_CHOICES, default=0)
    ocupacion = models.CharField(max_length=250, verbose_name=u'Ocupación', null=True, blank=True, default='')
    prevision_salud = models.IntegerField(verbose_name=u'Previsión de salud', null=True, blank=True, choices=PREVISION_SALUD_CHOICES, default=0)
    aporta_ingreso = models.BooleanField(default=False)
    calificacion_laboral = models.CharField(max_length=250, verbose_name=u'Calificación laboral', null=True, blank=True, choices=CALIFICACION_LABORAL_CHOICES, default="")

    familia = models.ForeignKey(Familia)

    principal = models.BooleanField(default=False)  # indica la persona que primero se ficho
    parentesco = models.IntegerField(null=True, blank=True, choices=PARENTESCO_CHOICES, default=0)  # parentesco con la persona principal, nulo si es el principal

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.nombres, self.apellido_paterno, self.apellido_materno)

    def get_fecha_nacimiento(self):
        if self.fecha_nacimiento is not None:
            if self.fecha_nacimiento != settings.NULL_DATE:
                return str(self.fecha_nacimiento)
            else:
                return None
        else:
            return None

    def get_color_btn_ficha(self, anio=None):
        """
        Establece el color del boton "Ficha" en la tabla de personas (ficha familiar)
        Gris: normal
        Verde: Ficha activa
        Negrita: Ficha cerrada
        """
        clase = 'btn-inactivo'

        if anio is None:
            anio = datetime.now().year

        for evaluacion in self.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio):
            if evaluacion.ciclo_cerrado:
                clase = 'btn-cerrado'
            elif evaluacion.objetivosevaluacion_set.count() > 0:
                clase = 'btn-success'

        return clase

    def tiene_ficha_activa(self, anio):
        ficha_activa = False
        for evaluacion in self.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio):
            if evaluacion.objetivosevaluacion_set.count() > 0:
                ficha_activa = True
                break
        return ficha_activa

    def get_estado(self):
        anio = datetime.now().year
        estado = ESTADO_FAMILIA_CHOICES[0][0]
        for evaluacion in self.evaluacionfactoresprotectores_set.filter(anio_aplicacion=anio):
            if evaluacion.objetivosevaluacion_set.count() > 0:
                estado = ESTADO_FAMILIA_CHOICES[1][0]
            if evaluacion.ciclo_cerrado:
                estado = ESTADO_FAMILIA_CHOICES[2][0]
        return estado

    def save(self, *args, **kwargs):
        super(Persona, self).save(*args, **kwargs)
        self.familia.save()


class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        exclude = ('calificacion_laboral', "date_created", "date_modified", 'fecha_participa', 'direccion')
        widgets = {
            'rut': RutInput(),
            'fecha_nacimiento': DateInput(attrs={'class': "datepicker"}),
            'fecha_participa': DateInput(attrs={'class': "datepicker"}),
            'fecha_ingreso': DateInput(attrs={'class': 'datepicker'}),
            'familia': forms.HiddenInput(),
            'ocupacion': forms.TextInput(attrs={"data-provide": "typeahead",
                                                "data-items": 4,
                                                "data-source": '[%s]' % (",".join('"%s"' % x for x in OCUPACION_CHOICES))})
        }


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        exclude = ('date_created', 'date_modified', 'estado')

        widgets = {
            'cond_precariedad': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_precariedad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_vulnerabilidad': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_vulnerabilidad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_hogar_uni_riesgo': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_hogar_uni_riesgo_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_familia_mono_riesgo': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_familia_mono_riesgo_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_alcohol_drogas': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_alcohol_drogas_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_discapacidad': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_discapacidad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_malos_tratos': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_malos_tratos_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_socializ_delictual': forms.RadioSelect(choices=PRESENTE_CHOICES, renderer=HorizontalRadio),
            'cond_socializ_delictual_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }


EVALUACION_CHOICES = (
    (-2, -2),
    (-1, -1),
    (0, 0),
    (1, 1),
    (2, 2),
    (-100, 'N/A'),
)


class Componentes(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre


class FactorProtector(models.Model):
    componente = models.ForeignKey(Componentes)
    factor_protector = models.CharField(max_length=250)
    objetivo_personal = models.TextField(null=True, blank=True)
    objetivo_grupal = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.factor_protector


class EvaluacionFactoresProtectores(models.Model):
    persona = models.ForeignKey(Persona)
    anio_aplicacion = models.IntegerField(verbose_name=u'Año de aplicación')

    # Datos de las tablas con los puntajes (Inicio):
    presencia_red_de_apoyo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Presencia red de apoyo')
    relaciones_con_vecindario = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Relaciones con vecindario')
    participacion_social = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación social')
    red_de_servicios_y_beneficios_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Red de servicios y beneficios sociales')
    ocio_y_encuentro_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Ocio y encuentro con pares')
    espacios_formativos_y_de_desarrollo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Espacios formativos y de desarrollo')
    relaciones_y_cohesion_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Relaciones y cohesión familiar')
    adaptabilidad_y_resistencia_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Adaptabilidad y resiliencia familiar')
    competencias_parentales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Competencias parentales')
    proteccion_y_salud_integral = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Protección y salud integral')
    participacion_protagonica = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación protagónica')
    recreacion_y_juego_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Recreación y juego con pares')
    crecimiento_personal = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Crecimiento personal')
    autonomia = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Autonomía')
    habilidades_y_valores_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Habilidades y valores sociales')

    # Datos de las tablas con los puntajes (Cumplimiento):
    presencia_red_de_apoyo2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Presencia red de apoyo')
    relaciones_con_vecindario2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Relaciones con vecindario')
    participacion_social2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación social')
    red_de_servicios_y_beneficios_sociales2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Red de servicios y beneficios sociales')
    ocio_y_encuentro_con_pares2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Ocio y encuentro con pares')
    espacios_formativos_y_de_desarrollo2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Espacios formativos y de desarrollo')
    relaciones_y_cohesion_familiar2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Relaciones y cohesión familiar')
    adaptabilidad_y_resistencia_familiar2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Adaptabilidad y resiliencia familiar')
    competencias_parentales2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Competencias parentales')
    proteccion_y_salud_integral2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Protección y salud integral')
    participacion_protagonica2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación protagónica')
    recreacion_y_juego_con_pares2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Recreación y juego con pares')
    crecimiento_personal2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Crecimiento personal')
    autonomia2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Autonomía')
    habilidades_y_valores_sociales2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Habilidades y valores sociales')

    # I.b
    propuesta_ciclo_desarrollo_socio_fam = models.TextField(verbose_name='Propuesta de Ciclo de Desarrollo Socio-Familiar', null=True, blank=True)

    # II.a
    tall_for_ori = models.BooleanField(verbose_name='Talleres de Formación y Orientación Familiar')

    tall_dep_rec = models.BooleanField(verbose_name='Talleres Deportivos Recreativos')
    tall_fut_cal = models.BooleanField(verbose_name='Talleres Fútbol Calle')
    tall_boccias = models.BooleanField(verbose_name='Talleres Boccias')
    tall_art_cul = models.BooleanField(verbose_name='Talleres Artísticos y Culturales')
    tall_ali_sal = models.BooleanField(verbose_name='Talleres de Alimentación Saludable')
    tall_hue_fam = models.BooleanField(verbose_name='Talleres de Huertos Familiares')

    enc_familiar = models.BooleanField(verbose_name='Encuentros Familiares')
    even_recreat = models.BooleanField(verbose_name='Eventos Recreativos')

    even_enc_cam = models.BooleanField(verbose_name='Eventos, Encuentros y Campeonatos Deportivos')
    even_dep_fam = models.BooleanField(verbose_name='Eventos Deportivos Familiares')
    even_cultura = models.BooleanField(verbose_name='Eventos Culturales')
    mues_fam_art = models.BooleanField(verbose_name='Muestras Familiares Artísticos-Culturales')
    enc_vida_sal = models.BooleanField(verbose_name='Encuentros de Vida Saludable')

    mod_form_fam = models.BooleanField(verbose_name='Módulos de Formación Familiar')
    acc_inf_difu = models.BooleanField(verbose_name='Acciones de Información y Difusión')
    aten_ind_fam = models.BooleanField(verbose_name='Atención Individual y Familiar')

    mod_clin_dep = models.BooleanField(verbose_name='Módulos y Clínicas Deportivas')
    acc_pase_vis = models.BooleanField(verbose_name='Acceso, Paseos, Visitas y Salidas Culturales')
    mod_clin_art = models.BooleanField(verbose_name='Módulos y Clínicas Artístico-Culturales')
    acc_recu_are = models.BooleanField(verbose_name='Acciones de Recuperación de Áreas Verdes')
    mod_clin_ali = models.BooleanField(verbose_name='Módulos y Clínicas de Alimentación Saludable, Huertos y Medioambiente')

    # II.b
    comentarios = models.TextField(null=True, blank=True)

    # II.d
    evaluacion_cualitativa = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    ciclo_cerrado = models.BooleanField(default=False)

    def cerrar_ciclo(self):

        # ciclo ya esta cerrado
        if self.ciclo_cerrado:
            return ""

        error_msg = "No se puede cerrar este ciclo debido a los siguientes errores: <br> <ul>"
        valid = True

        # --- validacion de factores protectores ---

        if self.presencia_red_de_apoyo is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('presencia_red_de_apoyo')[0].verbose_name

        if self.presencia_red_de_apoyo2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('presencia_red_de_apoyo2')[0].verbose_name

        if self.relaciones_con_vecindario is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('relaciones_con_vecindario')[0].verbose_name

        if self.relaciones_con_vecindario2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('relaciones_con_vecindario2')[0].verbose_name

        if self.participacion_social is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('participacion_social')[0].verbose_name

        if self.participacion_social2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('participacion_social2')[0].verbose_name

        if self.red_de_servicios_y_beneficios_sociales is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('red_de_servicios_y_beneficios_sociales')[0].verbose_name

        if self.red_de_servicios_y_beneficios_sociales2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('red_de_servicios_y_beneficios_sociales2')[0].verbose_name

        if self.ocio_y_encuentro_con_pares is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('ocio_y_encuentro_con_pares')[0].verbose_name

        if self.ocio_y_encuentro_con_pares2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('ocio_y_encuentro_con_pares2')[0].verbose_name

        if self.espacios_formativos_y_de_desarrollo is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('espacios_formativos_y_de_desarrollo')[0].verbose_name

        if self.espacios_formativos_y_de_desarrollo2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('espacios_formativos_y_de_desarrollo2')[0].verbose_name

        if self.relaciones_y_cohesion_familiar is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('relaciones_y_cohesion_familiar')[0].verbose_name

        if self.relaciones_y_cohesion_familiar2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('relaciones_y_cohesion_familiar2')[0].verbose_name

        if self.adaptabilidad_y_resistencia_familiar is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('adaptabilidad_y_resistencia_familiar')[0].verbose_name

        if self.adaptabilidad_y_resistencia_familiar2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('adaptabilidad_y_resistencia_familiar2')[0].verbose_name

        if self.competencias_parentales is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('competencias_parentales')[0].verbose_name

        if self.competencias_parentales2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('competencias_parentales2')[0].verbose_name

        if self.proteccion_y_salud_integral is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('proteccion_y_salud_integral')[0].verbose_name

        if self.proteccion_y_salud_integral2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('proteccion_y_salud_integral2')[0].verbose_name

        if self.participacion_protagonica is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('participacion_protagonica')[0].verbose_name

        if self.participacion_protagonica2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('participacion_protagonica2')[0].verbose_name

        if self.recreacion_y_juego_con_pares is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('recreacion_y_juego_con_pares')[0].verbose_name

        if self.recreacion_y_juego_con_pares2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('recreacion_y_juego_con_pares2')[0].verbose_name

        if self.crecimiento_personal is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('crecimiento_personal')[0].verbose_name

        if self.crecimiento_personal2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('crecimiento_personal2')[0].verbose_name

        if self.autonomia is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('autonomia')[0].verbose_name

        if self.autonomia2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('autonomia2')[0].verbose_name

        if self.habilidades_y_valores_sociales is None:
            valid = False
            error_msg += "<li>Factor protector '%s (I)' no ha sido evaluado</li>" % self._meta.get_field_by_name('habilidades_y_valores_sociales')[0].verbose_name

        if self.habilidades_y_valores_sociales2 is None:
            valid = False
            error_msg += "<li>Factor protector '%s (C)' no ha sido evaluado</li>" % self._meta.get_field_by_name('habilidades_y_valores_sociales2')[0].verbose_name

        # --- validacion objetivos ---
        if self.objetivosevaluacion_set.count() == 0:
            valid = False
            error_msg += "<li>Seleccione al menos un objetivo de desarrollo socio-familiar</li>"

        # --- validacion cumplimiento ---
        count_desarrollo = 0
        count_cultura = 0

        count_talleres = 0
        count_eventos = 0
        count_modulos = 0

        if self.tall_for_ori:
            count_desarrollo += 1
            count_talleres += 1
        if self.enc_familiar:
            count_desarrollo += 1
            count_eventos += 1
        if self.even_recreat:
            count_desarrollo += 1
            count_eventos += 1
        if self.mod_form_fam:
            count_desarrollo += 1
            count_modulos += 1
        if self.acc_inf_difu:
            count_desarrollo += 1
            count_modulos += 1
        if self.aten_ind_fam:
            count_desarrollo += 1
            count_modulos += 1

        if self.tall_dep_rec:
            count_cultura += 1
            count_talleres += 1
        if self.tall_fut_cal:
            count_cultura += 1
            count_talleres += 1
        if self.tall_boccias:
            count_cultura += 1
            count_talleres += 1
        if self.tall_art_cul:
            count_cultura += 1
            count_talleres += 1
        if self.tall_ali_sal:
            count_cultura += 1
            count_talleres += 1
        if self.tall_hue_fam:
            count_cultura += 1
            count_talleres += 1

        if self.even_enc_cam:
            count_cultura += 1
            count_eventos += 1
        if self.even_dep_fam:
            count_cultura += 1
            count_eventos += 1
        if self.even_cultura:
            count_cultura += 1
            count_eventos += 1
        if self.mues_fam_art:
            count_cultura += 1
            count_eventos += 1
        if self.enc_vida_sal:
            count_cultura += 1
            count_eventos += 1

        if self.mod_clin_dep:
            count_cultura += 1
            count_modulos += 1
        if self.acc_pase_vis:
            count_cultura += 1
            count_modulos += 1
        if self.mod_clin_art:
            count_cultura += 1
            count_modulos += 1
        if self.acc_recu_are:
            count_cultura += 1
            count_modulos += 1
        if self.mod_clin_ali:
            count_cultura += 1
            count_modulos += 1

        if count_desarrollo == 0 or count_cultura == 0:
            valid = False
            error_msg += u"<li>Debe seleccionar de ambos componentes ds intervención (columnas)</li>"

        if count_talleres == 0 or count_eventos == 0 or count_modulos == 0:
            valid = False
            error_msg += u"<li>Debe seleccionar al menos uno en cada area de trabajo (filas)</li>"

        # validacion completa: guardar
        if valid:
            self.ciclo_cerrado = True
            self.save()
            self.persona.familia.actualizar_estado(self.anio_aplicacion)
            error_msg = ""

        return error_msg

    def get_objetivos_ind(self):
        return self.objetivosevaluacion_set.filter(tipo=1)

    def get_objetivos_grup(self):
        return self.objetivosevaluacion_set.filter(tipo=2)

    def save(self, *args, **kwargs):
        super(EvaluacionFactoresProtectores, self).save(*args, **kwargs)
        for estado in self.persona.familia.estadofamiliaanio_set.all():
            estado.porcentaje_datos_parte2 = self.persona.familia.get_porcentaje_completo_p2(estado.anio)
            estado.porcentaje_datos_parte3 = self.persona.familia.get_porcentaje_completo_p3(estado.anio)
            estado.save()
        self.persona.save()


    class Meta:
        ordering = ['anio_aplicacion']


class ObjetivosEvaluacion(models.Model):
    evaluacion = models.ForeignKey(EvaluacionFactoresProtectores)
    factor = models.ForeignKey(FactorProtector)
    tipo = models.IntegerField(choices=OBJS_EVAL_CHOICES, default=1)


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = EvaluacionFactoresProtectores

        exclude = ("date_created", "date_modified")

        widgets = {
            'persona': forms.HiddenInput(),
            'anio_aplicacion': forms.HiddenInput(),
            #'objetivos_desarrollo_socio_fam': forms.HiddenInput(),
            'propuesta_ciclo_desarrollo_socio_fam': forms.Textarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
            'comentarios': forms.Textarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
            'talleres_grup_desarrollo_fam': forms.Textarea(attrs={'rows': 3}),
            'talleres_grup_cultura_salud': forms.Textarea(attrs={'rows': 3}),
            'eventos_y_enc_desarrollo_fam': forms.Textarea(attrs={'rows': 3}),
            'eventos_y_enc_cultura_salud': forms.Textarea(attrs={'rows': 3}),
            'modulos_acciones_desarrollo_fam': forms.Textarea(attrs={'rows': 3}),
            'modulos_acciones_cultura_salud': forms.Textarea(attrs={'rows': 3}),
            'evaluacion_cualitativa': forms.Textarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
        }


class EstadoFamiliaAnio(models.Model):
    familia = models.ForeignKey(Familia)
    anio = models.IntegerField()
    inactivo = models.BooleanField(default=True)
    activo = models.BooleanField(default=False)
    completo = models.BooleanField(default=False)
    porcentaje_datos_parte2 = models.FloatField(null=True, blank=True)
    porcentaje_datos_parte3 = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = (("familia", "anio"),)