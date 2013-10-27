from django.db import models
import json

class JsonField(models.TextField):

    description = "Transparently pack/unpack objects into JSON representations"

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):

        if isinstance(value, dict) or isinstance(value, list) or value is None:
            return value

        # check if the json elements are single quoted and change to correct quote:
        if value.find("'") != -1:
            value = value.replace("'", '"')

        # Intentionally, this is not in try because we don't want to allow assignations other
        # than json serializable objects (lists and dictionaries).
        # So this will raise exception in that case.
        return json.loads(value)

    def get_prep_value(self, value):
        if value is not None and (isinstance(value, dict) or isinstance(value, list)):
            return json.dumps(value)

        if self.null:
            return None
        else:
            return self.default
  