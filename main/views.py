# -*- encoding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from FichaFamilia.mensajes import DATOS_GUARDADOS
from main.models import *
from django.utils import simplejson
from django.core import serializers


def get_sort_link(columna, order_by, order_dir, page, page_size, filtros_params):

    if columna == order_by:
        # flip order
        order_dir = 'asc' if order_dir == 'desc' else 'desc'
    else:
        order_dir = 'desc' if order_dir == 'desc' else 'asc'

    link = "/?order_by=%s&order_dir=%s&page=%s&psize=%s&%s" % (columna, order_dir, page, page_size, filtros_params)

    return link


@login_required
def home(request):

    es_admin = request.user.is_superuser
    familias = Familia.objects.all()
    centros = CentroFamiliar.objects.all()
    tipos = TIPOS_FAMILIA_CHOICES
    estados = ESTADO_FAMILIA_CHOICES

    user_profile = request.user.get_profile()

    # --- Filtros ---
    num_ficha = request.GET.get('num_ficha', '')
    centro = request.GET.get('centro', '')
    apellidos = request.GET.get('apellidos', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')

    if not es_admin:
        centro = str(user_profile.centro_familiar.id)
        centro_familiar = user_profile.centro_familiar

    if num_ficha != '':
        num_ficha = int(num_ficha)
        familias = familias.filter(id=num_ficha)

    if centro != '':
        centro = int(centro)
        familias = familias.filter(centro_familiar=centro)

    if apellidos != '':
        familias = familias.filter(
            Q(apellido_materno__icontains=apellidos) |
            Q(apellido_paterno__icontains=apellidos)
        )

    if tipo != '':
        familias = familias.filter(tipo_de_familia=tipo)

    if estado != '':
        familias = familias.filter(estado=estado)

    filtros_params = 'num_ficha=%s&centro=%s&apellidos=%s&tipo=%s&estado=%s' % (num_ficha, centro, apellidos, tipo, estado)

    # --- Orden ---
    columnas_permitidas = ['id', 'centro_familiar', 'apellidos', 'tipo_de_familia', 'estado']
    order_by = request.GET.get('order_by', 'id')
    if order_by not in columnas_permitidas:
        order_by = 'id'
    order_dir = request.GET.get('order_dir', 'asc')
    if order_dir == 'desc':
        od = '-'
    else:
        od = ''

    if order_by == 'apellidos':
        familias = familias.order_by('%sapellido_paterno' % od, '%sapellido_materno' % od)
    else:
        familias = familias.order_by('%s%s' % (od, order_by))

    # --- Paginacion ---
    page = request.GET.get('page', 1)
    page_size = request.GET.get('psize', 20)

    try:
        page = int(page)
    except:
        page = 1

    try:
        page_size = int(page_size)
    except:
        page_size = 20

    paginator = Paginator(familias, page_size)

    try:
        familias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        familias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        familias = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    paginator_links_pref = "/?order_by=%s&order_dir=%s&psize=%s&%s" % (order_by, order_dir, page_size, filtros_params)
    psize_select_pref =    "/?order_by=%s&order_dir=%s&page=%s&%s" % (order_by, order_dir, page, filtros_params)

    page_link_lower = page - 5
    page_link_upper = page + 5

    # --- Links del header ---

    link_col_ficha = get_sort_link('id', order_by, order_dir, page, page_size, filtros_params)
    link_col_centro = get_sort_link('centro_familiar', order_by, order_dir, page, page_size, filtros_params)
    link_col_apellidos = get_sort_link('apellidos', order_by, order_dir, page, page_size, filtros_params)
    link_col_tipo = get_sort_link('tipo_de_familia', order_by, order_dir, page, page_size, filtros_params)
    link_col_estado = get_sort_link('estado', order_by, order_dir, page, page_size, filtros_params)

    current_querystring = "order_by=%s&order_dir=%s&page=%s&psize=%s&%s" % (order_by, order_dir, page, page_size, filtros_params)

    return render(request, 'home.html', locals())


@login_required
def familia(request, id):
    id = int(id)
    message = None
    message_class = ''
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    centro_familiar = None

    if not es_admin:
        centro = str(user_profile.centro_familiar.id)
        centro_familiar = user_profile.centro_familiar

    filters = []

    for name, val in request.GET.items():
        filters.append("%s=%s" % (name, val))

    back_url = "/?%s" % ("&".join(filters))

    try:
        familia = Familia.objects.get(id=id)
    except:
        familia = None

    if not es_admin:
        if familia.centro_familiar != centro_familiar:
            raise Http404

    if request.method == "POST":
        if familia is not None:
            familia_form = FamiliaForm(request.POST, instance=familia)
        else:
            familia_form = FamiliaForm(request.POST)  # post de una nueva

        if familia_form.is_valid():
            familia_form.save()
            message = DATOS_GUARDADOS
            message_class = 'success'
            if id == 0:
                return HttpResponseRedirect('/familia/%s%s' % (familia_form.instance.id, back_url))
    else:
        if familia is not None:
            familia_form = FamiliaForm(instance=familia)
        else:
            # agregar nuevo registro
            centro = user_profile.centro_familiar.id if user_profile.centro_familiar is not None else None
            familia_form = FamiliaForm(initial={'centro_familiar': centro})

    return render(request, 'ficha_familia.html', locals())


@login_required
def eliminar_familia(request, id):
    es_admin = request.user.is_superuser
    user_profile = request.user.get_profile()
    centro_familiar = None
    if not es_admin:
        centro_familiar = user_profile.centro_familiar

    filters = []

    for name, val in request.GET.items():
        filters.append("%s=%s" % (name, val))

    back_url = "/?%s" % ("&".join(filters))

    if request.method == 'POST':
        id = request.POST['id']

    try:
        familia = Familia.objects.get(id=id)
    except:
        raise Http404

    if not es_admin:
        if familia.centro_familiar != centro_familiar:
            raise Http404

    if request.method == 'POST':
        familia.delete()
        return HttpResponseRedirect(back_url)

    return render(request, 'eliminar_familia.html', locals())


@login_required
def eliminar_persona(request, id):
    es_admin = request.user.is_superuser
    user_profile = request.user.get_profile()
    centro_familiar = None
    if not es_admin:
        centro_familiar = user_profile.centro_familiar

    if request.method == 'POST':
        id = request.POST['id']

    try:
        persona = Persona.objects.get(id=id)
    except:
        raise Http404

    if not es_admin:
        if persona.familia.centro_familiar != centro_familiar:
            raise Http404

    filters = []

    for name, val in request.GET.items():
        filters.append("%s=%s" % (name, val))

    back_url = "/familia/%s/?%s" % (persona.familia.id, "&".join(filters))

    if request.method == 'POST':
        persona.delete()
        return HttpResponseRedirect(back_url)

    return render(request, 'eliminar_persona.html', locals())


@login_required
def get_persona_form(request, familia_id, id):
    es_admin = request.user.is_superuser
    user_profile = request.user.get_profile()
    centro_familiar = None
    if not es_admin:
        centro_familiar = user_profile.centro_familiar

    saved = False
    familia = Familia.objects.get(id=familia_id)

    if not es_admin:
        if familia.centro_familiar != centro_familiar:
            raise Http404

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

    form_html = render_to_string('persona_form.html', {'form': form})

    return HttpResponse(simplejson.dumps({'form': form_html, 'saved': saved, 'id': id}), content_type='application/json')


@login_required
def ficha(request, id, anio):
    try:
        persona = Persona.objects.get(id=id)
    except:
        raise Http404

    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    if not es_admin:
        centro = str(user_profile.centro_familiar.id)
        centro_familiar = user_profile.centro_familiar
        if persona.familia.centro_familiar != centro_familiar:
            raise Http404

    filters = []
    for name, val in request.GET.items():
        filters.append("%s=%s" % (name, val))

    str_filters = "&".join(filters)

    back_url = "/familia/%s/?%s" % (persona.familia.id, str_filters)

    # --- handle requests
    existe = False
    evaluacion = None
    message = None
    message_class = None

    componentes = Componentes.objects.all()
    factores_json = serializers.serialize("json", FactorProtector.objects.all())

    evaluacion_qs = EvaluacionFactoresProtectores.objects.filter(persona=persona, anio_aplicacion=anio)

    if evaluacion_qs.count():
        evaluacion = evaluacion_qs[0]

    if request.method == "POST":

        if evaluacion is not None:
            # update
            form = EvaluacionForm(request.POST, instance=evaluacion)
        else:
            # new
            form = EvaluacionForm(request.POST, initial={'persona': persona, 'anio_aplicacion': anio}, instance=evaluacion)

        if form.is_valid():

            valid = True

            # si anio es cero y evaluacion ya existe entonces error

            if str(anio) == '0':
                form_anio = form.cleaned_data['anio_aplicacion']
                if EvaluacionFactoresProtectores.objects.filter(persona=persona, anio_aplicacion=form_anio).count():
                    message = "La ficha para esta persona/año ya existe. Por favor vuelva a la página anterior y 1) Seleccione la ficha existente o 2) Cree una nueva ficha para un año diferente."
                    message_class = "error"
                    valid = False

            if valid:

                form.save()
                persona.familia.actualizar_estado()

                if evaluacion is None:
                    return HttpResponseRedirect("/ficha/%s/%s/?%s" % (persona.id, form.instance.anio_aplicacion, str_filters))

                # re-crear el form para q se muestren los cambios
                form = EvaluacionForm(instance=form.instance)

    else:
        if evaluacion is not None:
            # existe
            form = EvaluacionForm(instance=evaluacion)
        else:
            # nueva
            form = EvaluacionForm(initial={'persona': persona})

    return render(request, 'ficha_persona.html', locals())


def eliminar_ficha(request, id, anio):
    es_admin = request.user.is_superuser
    user_profile = request.user.get_profile()
    centro_familiar = None
    if not es_admin:
        centro_familiar = user_profile.centro_familiar

    try:
        persona = Persona.objects.get(id=id)
    except:
        raise Http404

    if not es_admin:
        if persona.familia.centro_familiar != centro_familiar:
            raise Http404

    try:
        evaluacion = EvaluacionFactoresProtectores.objects.get(persona=persona, anio_aplicacion=anio)
    except:
        raise Http404

    filters = []

    for name, val in request.GET.items():
        filters.append("%s=%s" % (name, val))

    back_url = "/ficha/%s/%s/?%s" % (persona.id, anio, "&".join(filters))

    if request.method == 'POST':
        id = request.POST['id']

        evaluacion.delete()
        return HttpResponseRedirect("/familia/%s/?%s" % (persona.familia.id, "&".join(filters)))

    return render(request, 'eliminar_ficha.html', locals())
