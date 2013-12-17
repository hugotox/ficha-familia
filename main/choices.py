# -*- encoding: UTF-8 -*-
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

EVALUACION_CHOICES = (
    (-2, -2),
    (-1, -1),
    (0, 0),
    (1, 1),
    (2, 2),
    (-100, 'N/A'),
)
