# -*- encoding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django import forms
from django.forms.widgets import DateInput
from main.fields import JsonField
from datetime import datetime
from utils.widgets import RutInput

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

SEXO_CHOICES = (('Masculino', 'Masculino'), ('Femenino', 'Femenino'))

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
    u'Otro'
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

    def __unicode__(self):
        return self.comuna


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    centro_familiar = models.ForeignKey(CentroFamiliar, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Familia(models.Model):
    apellido_materno = models.CharField(max_length=250)  # apellidos de la familia
    apellido_paterno = models.CharField(max_length=250)  # apellidos de la familia
    numero_integrantes = models.IntegerField(verbose_name=u'Número de integrantes', help_text='(que viven en el hogar)')
    ingreso_total_familiar = models.IntegerField(choices=INGRESO_TOTAL_CHOICES, null=True, blank=True)
    tipo_de_familia = models.IntegerField(choices=TIPOS_FAMILIA_CHOICES, null=True, blank=True)

    cond_precariedad = models.BooleanField(default=False, verbose_name=u'Condiciones de precariedad: vivienda, trabajo, situación sanitaria, otras.')
    cond_precariedad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_vulnerabilidad = models.BooleanField(default=False, verbose_name=u'Vulnerabilidad barrial (inseguridad, violencia, estigma, pocos accesos).')
    cond_vulnerabilidad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_hogar_uni_riesgo = models.BooleanField(default=False, verbose_name=u'Hogar unipersonal en situación de riesgo.')
    cond_hogar_uni_riesgo_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_familia_mono_riesgo = models.BooleanField(default=False, verbose_name=u'Familia monoparental en situación de riesgo.')
    cond_familia_mono_riesgo_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_alcohol_drogas = models.BooleanField(default=False, verbose_name=u'Consumo problemático de alcohol y/o drogas.')
    cond_alcohol_drogas_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_discapacidad = models.BooleanField(default=False, verbose_name=u'Presencia de discapacidad física y/o mental.')
    cond_discapacidad_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_malos_tratos = models.BooleanField(default=False, verbose_name=u'Experiencias de malos tratos (actual o histórica).')
    cond_malos_tratos_coment = models.CharField(max_length=250, null=True, blank=True)
    cond_socializ_delictual = models.BooleanField(default=False, verbose_name=u'Historial de socialización delictual (detenciones, problemas judiciales).')
    cond_socializ_delictual_coment = models.CharField(max_length=250, null=True, blank=True)

    centro_familiar = models.ForeignKey(CentroFamiliar, null=True, blank=True)
    estado = models.CharField(max_length=250, null=True, blank=True, choices=ESTADO_FAMILIA_CHOICES, default=ESTADO_FAMILIA_CHOICES[0][0])

    date_created = models.DateTimeField(default=datetime.now())
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.apellido_paterno, self.apellido_materno)

    def actualizar_estado(self):
        if self.estado == ESTADO_FAMILIA_CHOICES[0][0]:
            self.estado = ESTADO_FAMILIA_CHOICES[1][0]
            self.save()


class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellido_paterno = models.CharField(max_length=250)
    apellido_materno = models.CharField(max_length=250)
    rut = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=9, choices=SEXO_CHOICES, null=True, blank=True)
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
        return u'%s %s (Familia %s)' % (self.nombres, self.apellido_paterno, self.familia)


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ('calificacion_laboral', "date_created", "date_modified")
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
            'cond_precariedad': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_precariedad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_vulnerabilidad': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_vulnerabilidad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_hogar_uni_riesgo': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_hogar_uni_riesgo_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_familia_mono_riesgo': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_familia_mono_riesgo_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_alcohol_drogas': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_alcohol_drogas_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_discapacidad': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_discapacidad_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_malos_tratos': forms.RadioSelect(choices=PRESENTE_CHOICES),
            'cond_malos_tratos_coment': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'cond_socializ_delictual': forms.RadioSelect(choices=PRESENTE_CHOICES),
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

    # Datos de las tablas con los puntajes (I):
    presencia_red_de_apoyo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Presencia red de apoyo')
    relaciones_con_vecindario = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Relaciones con vecindario')
    participacion_social = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación social')
    red_de_servicios_y_beneficios_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Red de servicios y beneficios sociales')
    ocio_y_encuentro_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Ocio y encuentro con pares')
    espacios_formativos_y_de_desarrollo = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Espacios formativos y de desarrollo')
    relaciones_y_cohesion_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Relaciones y cohesión familiar')
    adaptabilidad_y_resistencia_familiar = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Adaptabilidad y resistencia familiar')
    competencias_parentales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Competencias parentales')
    proteccion_y_salud_integral = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Protección y salud integral')
    participacion_protagonica = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación protagónica')
    recreacion_y_juego_con_pares = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Recreación y juego con pares')
    crecimiento_personal = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Crecimiento personal')
    autonomia = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Autonomía')
    habilidades_y_valores_sociales = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Habilidades y valores sociales')

    # Datos de las tablas con los puntajes (C):
    presencia_red_de_apoyo2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Presencia red de apoyo')
    relaciones_con_vecindario2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Relaciones con vecindario')
    participacion_social2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Participación social')
    red_de_servicios_y_beneficios_sociales2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Red de servicios y beneficios sociales')
    ocio_y_encuentro_con_pares2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Ocio y encuentro con pares')
    espacios_formativos_y_de_desarrollo2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Espacios formativos y de desarrollo')
    relaciones_y_cohesion_familiar2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name=u'Relaciones y cohesión familiar')
    adaptabilidad_y_resistencia_familiar2 = models.IntegerField(choices=EVALUACION_CHOICES, null=True, blank=True, verbose_name='Adaptabilidad y resistencia familiar')
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
