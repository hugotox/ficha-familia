# -*- encoding: UTF-8 -*-

from django.db import models
from django import forms


class Familia(models.Model):
    identificador = models.CharField(max_length=250, null=True, blank=True)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes en la familia (que viven en el hogar)')
    ingreso_total_familiar = models.CharField(max_length=250, choices=(('0-100.000', '0-100.000'), ('100.000-200.000', '100.000-200.000'), ('100.000-200.000', '200.000-300.000'), (u'300.000-más', u'300.000-más'),), null=True, blank=True)
    tipo_de_familia = models.CharField(max_length=250, choices=(('Nuclear', 'Nuclear'), ('Monoparental', 'Monoparental'), ('Extendida', 'Extendida'), ('Unipersonal', 'Unipersonal')), null=True, blank=True)
    tipo_mono = models.CharField(max_length=250, choices=(('Padre', 'Padre'), ('Madre', 'Madre'), ('Abuelo(a)', 'Abuelo(a)'), ('Otro Adulto Responsable', 'Otro Adulto Responsable')), null=True, blank=True)
    tipo_otra = models.CharField(max_length=250, null=True, blank=True)

    condiciones_precariedad = models.BooleanField(default=False)
    condiciones_vulnerabilidad = models.BooleanField(default=False)
    condiciones_hogar_uni_riesgo = models.BooleanField(default=False)
    condiciones_familia_mono_riesgo = models.BooleanField(default=False)
    condiciones_alcohol_drogas = models.BooleanField(default=False)
    condiciones_discapacidad = models.BooleanField(default=False)
    condiciones_malos_tratos = models.BooleanField(default=False)
    condiciones_socializ_delictual = models.BooleanField(default=False)


class Persona(models.Model):
    nombres = models.CharField(max_length=250, null=True, blank=True)
    apellidos = models.CharField(max_length=250, null=True, blank=True)
    rut = models.CharField(max_length=12, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=9, choices=(('Masculino', 'Masculino'), ('Femenino', 'Femenino')), null=True, blank=True)
    direccion = models.CharField(max_length=250, verbose_name=u'Dirección', null=True, blank=True)
    telefono = models.CharField(max_length=250, verbose_name=u'Teléfono de contacto', null=True, blank=True)
    fecha_ingreso = models.DateField(verbose_name='Desde cuándo participa en FF', null=True, blank=True)

    estado_civil = models.CharField(max_length=250, null=True, blank=True)
    nivel_escolaridad = models.CharField(max_length=250, null=True, blank=True)
    ocupacion = models.CharField(max_length=250, verbose_name=u'Ocupación', null=True, blank=True)
    prevision_salud = models.CharField(max_length=250, verbose_name=u'Previsión de salud', null=True, blank=True)
    aporta_ingreso = models.BooleanField(default=False)
    calificacion_laboral = models.CharField(max_length=250, verbose_name=u'Calificación laboral', null=True, blank=True)

    familia = models.ForeignKey(Familia, null=True, blank=True)

    parientes = models.ManyToManyField("Persona", through="Parentesco", null=True, blank=True)


class Parentesco(models.Model):
    persona1 = models.ForeignKey(Persona, related_name='persona1')
    persona2 = models.ForeignKey(Persona, related_name='persona2')
    parentesco = models.CharField(max_length=250)


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'class': 'datepicker'}),
            'fecha_ingreso': forms.TextInput(attrs={'class': 'datepicker'}),
        }


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia


EVALUACION_CHOICES = (
    (2, 2),
    (1, 1),
    (0, 0),
    (-1, -1),
    (-2, -2),
    (0, 'N/A'),
)


class EvaluacionFactoresProtectores(models.Model):
    presencia_red_de_apoyo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    relaciones_con_vecindario = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    participacion_social = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    red_de_servicios_y_beneficios_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    ocio_y_encuentro_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    espacios_formativos_y_de_desarrollo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    relaciones_y_cohesion_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    adaptabilidad_y_resistencia_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    competencias_parentales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    proteccion_y_salud_integral = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    participacion_protagonica = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    recreacion_y_juego_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    crecimiento_personal = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    autonomia = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)
    habilidades_y_valores_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True)


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = EvaluacionFactoresProtectores