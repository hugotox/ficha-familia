from django.test import TestCase


class BaseTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertStatus200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertStatusRedirect(self, response):
        self.assertEqual(response.status_code, 302)