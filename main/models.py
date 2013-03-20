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
    (u'Enseñanza Preescolar', u'Enseñanza Preescolar'),
    (u'Enseñanza Básica Incompleta', u'Enseñanza Básica Incompleta'),
    (u'Enseñanza Básica Completa', u'Enseñanza Básica Completa'),
    (u'Enseñanza Media Incompleta', u'Enseñanza Media Incompleta'),
    (u'Enseñanza Media Completa', u'Enseñanza Media Completa'),
    (u'Técnica Incompleta', u'Técnica Incompleta'),
    (u'Técnico Completa', u'Técnico Completa'),
    (u'Universitaria Incompleta', u'Universitaria Incompleta'),
    (u'Universitaria Completa', u'Universitaria Completa'),
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
    ('0-100.000', '0-100.000'),
    ('100.000-200.000', '100.000-200.000'),
    ('100.000-200.000', '200.000-300.000'),
    (u'300.000-más', u'300.000-más')
)

TIPOS_FAMILIA_CHOICES = (
    ('Nuclear', 'Nuclear'),
    ('Monoparental', 'Monoparental'),
    ('Extendida', 'Extendida'),
    ('Unipersonal', 'Unipersonal'),
    ('Otra', 'Otra')
)

TIPOS_FAMILIA_MONO_CHOICES = (
    ('Padre', 'Padre'),
    ('Madre', 'Madre'),
    ('Abuelo(a)', 'Abuelo(a)'),
    ('Otro Adulto Responsable', 'Otro Adulto Responsable')
)

SEXO_CHOICES = (('Masculino', 'Masculino'), ('Femenino', 'Femenino'))

ESTADO_CIVIL_CHOICES = (
    ('Soltero', 'Soltero'),
    ('Casado', 'Casado'),
    ('Viudo', 'Viudo'),
    ('Separado Judicialmente', 'Separado Judicialmente'),
    ('Divorciado', 'Divorciado')
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
    apellidos = models.CharField(max_length=250)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes', help_text='(que viven en el hogar)')
    ingreso_total_familiar = models.CharField(max_length=250, choices=INGRESO_TOTAL_CHOICES, null=True, blank=True)
    tipo_de_familia = models.CharField(max_length=250, choices=TIPOS_FAMILIA_CHOICES, null=True, blank=True)
    tipo_mono = models.CharField(max_length=250, choices=TIPOS_FAMILIA_MONO_CHOICES, null=True, blank=True, verbose_name='Tipo Monoparental')

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
        return u'%s' % self.apellidos


class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellido_paterno = models.CharField(max_length=250)
    apellido_materno = models.CharField(max_length=250)
    rut = models.CharField(max_length=12, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=9, choices=SEXO_CHOICES, null=True, blank=True)
    direccion = models.CharField(max_length=250, verbose_name=u'Dirección', null=True, blank=True)
    telefono = models.CharField(max_length=250, verbose_name=u'Teléfono de contacto', null=True, blank=True)
    fecha_ingreso = models.DateField(verbose_name='Desde cuándo participa en FF', null=True, blank=True)

    estado_civil = models.CharField(max_length=250, null=True, blank=True, choices=ESTADO_CIVIL_CHOICES)
    nivel_escolaridad = models.CharField(max_length=250, null=True, blank=True, choices=NIVEL_ESC_CHOICES)
    ocupacion = models.CharField(max_length=250, verbose_name=u'Ocupación', null=True, blank=True, choices=OCUPACION_CHOICES)
    prevision_salud = models.CharField(max_length=250, verbose_name=u'Previsión de salud', null=True, blank=True)
    aporta_ingreso = models.BooleanField(default=False)
    calificacion_laboral = models.CharField(max_length=250, verbose_name=u'Calificación laboral', null=True, blank=True, choices=CALIFICACION_LABORAL_CHOICES)

    familia = models.ForeignKey(Familia)

    principal = models.BooleanField(default=False)  # indica la persona que primero se ficho
    parentesco = models.CharField(max_length=150, null=True, blank=True)  # parentesco con la persona principal, nulo si es el principal

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
