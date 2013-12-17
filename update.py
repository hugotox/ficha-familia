# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

cursor = connection.cursor()
sql = '''
    DROP TABLE main_estadofamiliaanio;
'''
cursor.execute(sql)
transaction.commit_unless_managed()




print "All done"
