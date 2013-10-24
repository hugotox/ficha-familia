# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

cursor = connection.cursor()
sql = '''
   update main_familia set porcentaje_datos_parte1=null;
'''
cursor.execute(sql)
transaction.commit_unless_managed()


for familia in Familia.objects.all():
    familia.save()
    print 'Familia %s ok.' % familia


print "All done"
