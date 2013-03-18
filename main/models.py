# -*- encoding: UTF-8 -*-
from django.contrib.auth.models import User

from django.db import models
from django import forms

BOOLEAN_CHOICES = (
    (True, u'Sí'),
    (False, u'No'),
)

class Familia(models.Model):
    apellidos = models.CharField(max_length=250)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes', help_text='(que viven en el hogar)')
    ingreso_total_familiar = models.CharField(max_length=250, choices=(('0-100.000', '0-100.000'), ('100.000-200.000', '100.000-200.000'), ('100.000-200.000', '200.000-300.000'), (u'300.000-más', u'300.000-más'),), null=True, blank=True)
    tipo_de_familia = models.CharField(max_length=250, choices=(('Nuclear', 'Nuclear'), ('Monoparental', 'Monoparental'), ('Extendida', 'Extendida'), ('Unipersonal', 'Unipersonal')), null=True, blank=True)
    tipo_mono = models.CharField(max_length=250, choices=(('Padre', 'Padre'), ('Madre', 'Madre'), ('Abuelo(a)', 'Abuelo(a)'), ('Otro Adulto Responsable', 'Otro Adulto Responsable')), null=True, blank=True)
    tipo_otra = models.CharField(max_length=250, null=True, blank=True, verbose_name='Otra')

    cond_precariedad = models.BooleanField(default=False, verbose_name=u'Condiciones de precariedad: vivienda, trabajo, situación sanitaria, otras.')
    cond_vulnerabilidad = models.BooleanField(default=False, verbose_name=u'Vulnerabilidad barrial (inseguridad, violencia, estigma, pocos accesos).')
    cond_hogar_uni_riesgo = models.BooleanField(default=False, verbose_name=u'Hogar unipersonal en situación de riesgo.')
    cond_familia_mono_riesgo = models.BooleanField(default=False, verbose_name=u'Familia monoparental en situación de riesgo.')
    cond_alcohol_drogas = models.BooleanField(default=False, verbose_name=u'Consumo problemático de alcohol y/o drogas.')
    cond_discapacidad = models.BooleanField(default=False, verbose_name=u'Presencia de discapacidad física y/o mental.')
    cond_malos_tratos = models.BooleanField(default=False, verbose_name=u'Experiencias de malos tratos (actual o histórica).')
    cond_socializ_delictual = models.BooleanField(default=False, verbose_name=u'Historial de socialización delictual (detenciones, problemas judiciales).')

    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.apellidos


class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellido_paterno = models.CharField(max_length=250)
    apellido_materno = models.CharField(max_length=250)
    rut = models.CharField(max_length=12, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)  # TODO: formato de entrada en fecha
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

    familia = models.ForeignKey(Familia)

    def __unicode__(self):
        return u'%s %s (Familia %s)' % (self.nombres, self.apellido_paterno, self.familia)

    def get_parientes(self):
        personas_en_familia = list(self.familia.persona_set.exclude(id=self.id))

        # agregar los parientes q son familia y no estan en la lista de parientes
        parientes = [x.pariente for x in self.persona.all()]
        for per in personas_en_familia:
            if per not in parientes:
                self.agregar_pariente(per, "")
                parientes.append(per)

        return parientes

    def agregar_pariente(self, pariente, parentesco):
        self.persona.create(persona=self, pariente=pariente, parentesco=parentesco)

    def save(self, *args, **kwargs):
        super(Persona, self).save(*args, **kwargs)
        self.get_parientes()  # provoca actualizar los parientes en base a la familia


class Parentesco(models.Model):
    persona = models.ForeignKey(Persona, related_name='persona')  # persona en la ficha
    pariente = models.ForeignKey(Persona, related_name='pariente')  # pariente
    parentesco = models.CharField(max_length=250)


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'class': 'datepicker'}),
            'fecha_ingreso': forms.TextInput(attrs={'class': 'datepicker'}),
            'familia': forms.HiddenInput()
        }


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        exclude = ('date_created', 'date_modified')

        widgets = {
            'cond_precariedad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_vulnerabilidad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_hogar_uni_riesgo': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_familia_mono_riesgo': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_alcohol_drogas': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_discapacidad': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_malos_tratos': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'cond_socializ_delictual': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'created_by': forms.HiddenInput()
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
    etapa = models.CharField(max_length=20, choices=(('inicio', 'Inicio'), ('cumplimiento', 'Cumplimiento')))
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
