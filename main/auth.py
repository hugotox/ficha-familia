# -*- encoding: UTF-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django import forms
from mensajes import CUENTA_EXPIRADA, LOGIN_ERR


class ChangePasswordForm(forms.Form):
    current = forms.CharField(label=u'Contraseña actual', widget=forms.PasswordInput())
    new_pass = forms.CharField(label=u'Nueva contraseña', widget=forms.PasswordInput())
    confirm = forms.CharField(label=u'Confirme nueva contraseña', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('user'):
            self.user = kwargs.pop('user')
        else:
            raise Exception("Por favor incluya el objeto 'user' dentro de kwargs")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        the_data = self.cleaned_data
        current = the_data.get('current')
        new_pass = the_data.get('new_pass')
        confirm = the_data.get('confirm')

        if new_pass != confirm:
            raise forms.ValidationError(u"Las contraseñas no coinciden.")

        if not self.user.check_password(current):
            raise forms.ValidationError(u"La contraseña actual es incorrecta.")

        return the_data

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

@login_required
def changepasswd(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_pass'])
            request.user.save()
            success = True
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'changepasswd.html', locals())