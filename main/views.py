# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import PersonaForm, FamiliaForm


@login_required
def home(request):
    form = PersonaForm()
    familia_form = FamiliaForm()
    return render_to_response('home.html', {'form': form, 'familia_form': familia_form}, context_instance=RequestContext(request))