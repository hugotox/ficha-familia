# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

for familia in Familia.objects.all():
    print familia.get_estado(True)