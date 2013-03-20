# -*- encoding: UTF-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase


class FichaFamiliaTests(TestCase):

    def do_login(self):
        user = User.objects.create_user('hugo', 'hugo@hugotox.com', '123123')
        resp = self.client.post("/accounts/login/", data={'username': 'hugo', 'password': '123123'})
        self.assertEqual(resp.status_code, 302)  # redirect al home
        return user

    def test_home_not_logged_user(self):
        # 1. test redirect al login
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)

        # 2. test login
        resp = self.client.get("/accounts/login/")
        self.assertContains(resp, "id_username")
        self.assertContains(resp, "id_password")

    def test_home(self):
        user = self.do_login()
        resp = self.client.get("/")
        self.assertContains(resp, "Listado de Familias")