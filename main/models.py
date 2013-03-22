# -*- encoding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django import forms
from django.forms.widgets import DateInput

BOOLEAN_CHOICES = (
    (True, u'Sí'),
    (False, u'No'),
)

NIVEL_ESC_CHOICES = (
    (0, 'Sin Información'),
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

SEXO_CHOICES = (('Masculino', 'Masculino'), ('Femenino', 'Femenino'))

ESTADO_CIVIL_CHOICES = (
    (0, 'Sin Información'),
    (1, 'Soltero (a)'),
    (2, 'Casado (a)'),
    (3, 'Viudo (a)'),
    (4, 'Separado (a)'),
    (5, 'Convive'),
)

ETAPA_EVAL_CHOICES = (('inicio', 'Inicio'), ('cumplimiento', 'Cumplimiento'))

OCUPACION_CHOICES = (
    (u'Dueña de casa', u'Dueña de casa'),
    (u'Empleado', u'Empleado'),
    (u'Comerciante', u'Comerciante'),
    (u'Obrero', u'Obrero'),
    (u'Otro', u'Otro'),
)

ESTADO_FAMILIA_CHOICES = (
    ('No trabajada', 'No trabajada'),
    ('Vigente', 'Vigente'),
    ('Cerrada', 'Cerrada')
)

PREVISION_SALUD_CHOICES = (
    (0, 'Sin Información'),
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

    def __unicode__(self):
        return self.comuna


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    centro_familiar = models.ForeignKey(CentroFamiliar, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Familia(models.Model):
    apellido_materno = models.CharField(max_length=250)  # apellidos de la familia
    apellido_paterno = models.CharField(max_length=250)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes', help_text='(que viven en el hogar)')
    ingreso_total_familiar = models.IntegerField(choices=INGRESO_TOTAL_CHOICES, null=True, blank=True)
    tipo_de_familia = models.IntegerField(choices=TIPOS_FAMILIA_CHOICES, null=True, blank=True)

    cond_precariedad = models.BooleanField(default=False, verbose_name=u'Condiciones de precariedad: vivienda, trabajo, situación sanitaria, otras.')
    cond_vulnerabilidad = models.BooleanField(default=False, verbose_name=u'Vulnerabilidad barrial (inseguridad, violencia, estigma, pocos accesos).')
    cond_hogar_uni_riesgo = models.BooleanField(default=False, verbose_name=u'Hogar unipersonal en situación de riesgo.')
    cond_familia_mono_riesgo = models.BooleanField(default=False, verbose_name=u'Familia monoparental en situación de riesgo.')
    cond_alcohol_drogas = models.BooleanField(default=False, verbose_name=u'Consumo problemático de alcohol y/o drogas.')
    cond_discapacidad = models.BooleanField(default=False, verbose_name=u'Presencia de discapacidad física y/o mental.')
    cond_malos_tratos = models.BooleanField(default=False, verbose_name=u'Experiencias de malos tratos (actual o histórica).')
    cond_socializ_delictual = models.BooleanField(default=False, verbose_name=u'Historial de socialización delictual (detenciones, problemas judiciales).')

    centro_familiar = models.ForeignKey(CentroFamiliar, null=True, blank=True)
    estado = models.CharField(max_length=250, null=True, blank=True, choices=ESTADO_FAMILIA_CHOICES, default=ESTADO_FAMILIA_CHOICES[0][0])

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.apellido_paterno, self.apellido_materno)


class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellido_paterno = models.CharField(max_length=250)
    apellido_materno = models.CharField(max_length=250)
    rut = models.CharField(max_length=12, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=9, choices=SEXO_CHOICES, null=True, blank=True)
    direccion = models.CharField(max_length=250, verbose_name=u'Dirección', null=True, blank=True)
    telefono = models.CharField(max_length=250, verbose_name=u'Teléfono de contacto', null=True, blank=True)
    fecha_participa = models.DateField(verbose_name='Desde cuándo participa en FF', null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)

    estado_civil = models.IntegerField(null=True, blank=True, choices=ESTADO_CIVIL_CHOICES, default=0)
    nivel_escolaridad = models.IntegerField(null=True, blank=True, choices=NIVEL_ESC_CHOICES, default=0)
    ocupacion = models.CharField(max_length=250, verbose_name=u'Ocupación', null=True, blank=True, choices=OCUPACION_CHOICES)
    prevision_salud = models.IntegerField(verbose_name=u'Previsión de salud', null=True, blank=True, choices=PREVISION_SALUD_CHOICES, default=0)
    aporta_ingreso = models.BooleanField(default=False)
    calificacion_laboral = models.CharField(max_length=250, verbose_name=u'Calificación laboral', null=True, blank=True, choices=CALIFICACION_LABORAL_CHOICES)

    familia = models.ForeignKey(Familia)

    principal = models.BooleanField(default=False)  # indica la persona que primero se ficho
    parentesco = models.IntegerField(null=True, blank=True, choices=PARENTESCO_CHOICES, default=0)  # parentesco con la persona principal, nulo si es el principal

    def __unicode__(self):
        return u'%s %s (Familia %s)' % (self.nombres, self.apellido_paterno, self.familia)


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        widgets = {
            'fecha_nacimiento': DateInput(attrs={'class': "datepicker"}),
            'fecha_ingreso': DateInput(attrs={'class': 'datepicker'}),
            'familia': forms.HiddenInput()
        }


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        exclude = ('date_created', 'date_modified', 'estado')

        widgets = {
            'cond_precariedad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_vulnerabilidad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_hogar_uni_riesgo': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_familia_mono_riesgo': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_alcohol_drogas': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_discapacidad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_malos_tratos': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_socializ_delictual': forms.RadioSelect(choices=BOOLEAN_CHOICES),
        }


EVALUACION_CHOICES = (
    (2, 2),
    (1, 1),
    (0, 0),
    (-1, -1),
    (-2, -2),
    (-100, 'N/A'),
)


class EvaluacionFactoresProtectores(models.Model):
    persona = models.ForeignKey(Persona)
    anio_aplicacion = models.IntegerField(verbose_name=u'Año de aplicación')
    etapa = models.CharField(max_length=20, choices=ETAPA_EVAL_CHOICES)
    presencia_red_de_apoyo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    relaciones_con_vecindario = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    participacion_social = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación social')
    red_de_servicios_y_beneficios_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    ocio_y_encuentro_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    espacios_formativos_y_de_desarrollo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    relaciones_y_cohesion_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Relaciones y cohesión familiar')
    adaptabilidad_y_resistencia_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    competencias_parentales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    proteccion_y_salud_integral = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Protección y salud integral')
    participacion_protagonica = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación protagónica')
    recreacion_y_juego_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Recreación y juego con pares')
    crecimiento_personal = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    autonomia = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Autonomía')
    habilidades_y_valores_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = EvaluacionFactoresProtectores

        widgets = {
            'persona': forms.HiddenInput()
        }

# class PlanDeDesarrollo(models.Model):
#     familia = models.ForeignKey(Familia)
