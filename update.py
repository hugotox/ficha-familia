# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.models import *
from django.db import connection, transaction

sql = """
CREATE TABLE "main_estadofamiliaanio" (
    "id" serial NOT NULL PRIMARY KEY,
    "familia_id" integer NOT NULL REFERENCES "main_familia" ("id") DEFERRABLE INITIALLY DEFERRED,
    "anio" integer NOT NULL
);

CREATE INDEX "main_estadofamiliaanio_familia_id" ON "main_estadofamiliaanio" ("familia_id");
"""