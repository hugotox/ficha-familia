from unit_tests.base import BaseTestCase


class ViewsTests(BaseTestCase):

    def test_home(self):
        # no logueado debe responder un redirect
        resp = self.client.get("/")
        self.assertStatusRedirect(resp)
