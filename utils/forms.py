# -*- encoding: UTF-8 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Nombre de usuario")
    password = forms.CharField(required=True, label=u"Contraseña", widget=forms.PasswordInput)