# -*- encoding: UTF-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection, transaction

sql = """
CREATE TABLE main_estadofamiliaanio
(
  id serial NOT NULL,
  familia_id integer NOT NULL,
  anio integer NOT NULL,
  estado character varying(250),
  CONSTRAINT main_estadofamiliaanio_pkey PRIMARY KEY (id),
  CONSTRAINT main_estadofamiliaanio_familia_id_fkey FOREIGN KEY (familia_id)
      REFERENCES main_familia (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT main_estadofamiliaanio_familia_id_anio_key UNIQUE (familia_id, anio)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX main_estadofamiliaanio_familia_id
  ON main_estadofamiliaanio
  USING btree
  (familia_id);

INSERT INTO main_estadofamiliaanio (familia_id, anio, estado) select f.id, 2013, f.estado from main_familia f;
"""

cursor = connection.cursor()
cursor.execute(sql)
transaction.commit_unless_managed()

print "All done"