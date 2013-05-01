from django.forms import TextInput
from utils.formatters import format_rut


class RutInput(TextInput):
    def _format_value(self, value):
        return format_rut(value)