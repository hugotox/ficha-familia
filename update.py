# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *

EstadoFamiliaAnio.objects.all().delete()

for familia in Familia.objects.all():
    familia.actualizar_estado(2013)

print "All done"