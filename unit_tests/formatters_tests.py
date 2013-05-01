from unit_tests.base import BaseTestCase
from utils.formatters import format_rut


class FormaRutTest(BaseTestCase):

    def test_format_rut(self):
        self.assertEqual(format_rut("156844667"), "15.684.466-7")
        self.assertEqual(format_rut("98770364"), "9.877.036-4")
