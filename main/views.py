# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from tastypie.http import HttpNotFound
from main.models import PersonaForm, FamiliaForm, Familia, Persona
from django.utils import simplejson


@login_required
def home(request):

    order_by = request.GET.get('order_by', 'apellidos')

    search_query = request.GET.get('q', '')

    familias = Familia.objects.all()

    if not request.user.is_superuser:
        familias = familias.filter(created_by=request.user)

    if search_query != '':
        familias = familias.filter(apellidos__icontains=search_query)

    familias = familias.order_by(order_by)

    page = request.GET.get('page', 1)

    paginator = Paginator(familias, 20) # 20 familias por pagina

    try:
        familias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        familias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        familias = paginator.page(paginator.num_pages)

    return render(request, 'home.html', locals())


@login_required
def familia(request, id):
    id = int(id)

    try:
        familia = Familia.objects.get(id=id)
    except:
        familia = None

    if request.method == "POST":
        if familia is not None:
            familia_form = FamiliaForm(request.POST, instance=familia)
        else:
            familia_form = FamiliaForm(request.POST)  # post de una nueva

        if familia_form.is_valid():
            familia_form.save()
            if id == 0:
                return HttpResponseRedirect('/familia/%s' % familia_form.instance.id)
    else:
        if familia is not None:
            familia_form = FamiliaForm(instance=familia)
        else:
            # agregar nuevo registro
            familia_form = FamiliaForm(initial={'created_by': request.user})

    return render(request, 'ficha_familia.html', {'familia': familia, 'familia_form': familia_form})


@login_required
def ficha(request, id):
    try:
        persona = Persona.objects.get(id=id)
    except:
        return HttpNotFound()
    form = PersonaForm(instance=persona)
    return render(request, 'ficha_persona.html', locals())


@login_required
def eliminar_familia(request, id):

    if request.method == 'POST':
        id = request.POST['id']

    try:
        familia = Familia.objects.get(id=id)
    except:
        return HttpNotFound()

    if request.method == 'POST':
        familia.delete()
        return HttpResponseRedirect('/')

    return render(request, 'eliminar_familia.html', locals())

@login_required
def eliminar_persona(request, id):
    next = request.GET.get('next', '/')
    if request.method == 'POST':
        id = request.POST['id']

    try:
        persona = Persona.objects.get(id=id)
    except:
        return HttpNotFound()

    if request.method == 'POST':
        persona.delete()
        return HttpResponseRedirect(next)

    return render(request, 'eliminar_persona.html', locals())


@login_required
def get_persona_form(request, familia_id,  id):

    saved = False
    familia = Familia.objects.get(id=familia_id)

    id = int(id)

    if id == 0:
        persona = None
    else:
        persona = Persona.objects.get(id=id)

    if request.method == "POST":
        if persona is not None:
            form = PersonaForm(request.POST, instance=persona)
        else:
            form = PersonaForm(request.POST)

        if form.is_valid():
            form.save()
            saved = True
            id = form.instance.id

    else:

        if persona is not None:
            form = PersonaForm(instance=persona)
        else:
            form = PersonaForm(initial={'familia': familia})

    return HttpResponse(simplejson.dumps({'form': form.as_table(), 'saved': saved, 'id': id}), content_type='application/json')