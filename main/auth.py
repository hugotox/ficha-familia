# -*- encoding: UTF-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from FichaFamilia.mensajes import CUENTA_EXPIRADA, LOGIN_ERR


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Nombre de usuario")
    password = forms.CharField(required=True, label=u"Contraseña", widget=forms.PasswordInput)


def login_view(request):

    msg_error = None

    if request.method == "POST":

        next_page = request.GET.get("next", "/")

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect(next_page)
                else:
                    # Return a 'disabled account' error message
                    msg_error = CUENTA_EXPIRADA
            else:
                # Return an 'invalid login' error message.
                msg_error = LOGIN_ERR

    else:

        form = LoginForm()


    return render_to_response('login.html', {'form': form, 'msg_error': msg_error}, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")