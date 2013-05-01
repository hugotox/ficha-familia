from unit_tests.base import BaseTestCase
from utils.validators import validate_rut


class ValidateRutTest(BaseTestCase):

    def test_valid_rut(self):
        # Ruts validos:
        ruts = [
            '156844667',
            '15.684.466-7',
            '15684466-7',
            '98770364',
            '9877036-4',
            '9.877.036-4',
            '9677611k',
            '9677611-k',
            '9.677.611-k',
        ]

        for rut in ruts:
            self.assertTrue(validate_rut(rut))

    def test_invalid_rut(self):
        # Ruts invalidos:
        ruts = [
            '156844668',
            '15684n4668',
            '14.684.466-7',
            '15684466-k',
            '98a70364',
            '9877036-5',
            '9.87k.036-4',
            '967761177',
            '96776g1-k',
            '1.677.611-k',
        ]

        for rut in ruts:
            self.assertFalse(validate_rut(rut))