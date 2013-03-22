# -*- encoding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from FichaFamilia.mensajes import DATOS_GUARDADOS
from main.models import PersonaForm, FamiliaForm, Familia, Persona, EvaluacionForm, CentroFamiliar, TIPOS_FAMILIA_CHOICES, ESTADO_FAMILIA_CHOICES
from django.utils import simplejson


def get_sort_link(columna, order_by, order_dir, page, page_size):

    if columna == order_by:
        # flip order
        order_dir = 'asc' if order_dir == 'desc' else 'desc'
    else:
        order_dir = 'desc' if order_dir == 'desc' else 'asc'

    link = "/?order_by=%s&order_dir=%s&page=%s&psize=%s" % (columna, order_dir, page, page_size)

    return link

@login_required
def home(request):

    es_admin = request.user.is_superuser
    familias = Familia.objects.all()
    centros = CentroFamiliar.objects.all()
    tipos = TIPOS_FAMILIA_CHOICES
    estados = ESTADO_FAMILIA_CHOICES

    # --- Filtros ---
    if request.method == "POST":
        num_ficha = request.POST.get('num_ficha', '')
        centro = request.POST.get('centro', '')
        apellidos = request.POST.get('apellidos', '')
        tipo = request.POST.get('tipo', '')
        estado = request.POST.get('estado', '')

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

    else:
        num_ficha = ''
        centro = ''
        apellidos = ''
        tipo = ''
        estado = ''

    if not es_admin:
        user_profile = request.user.get_profile()
        familias = familias.filter(centro_familiar=user_profile.centro_familiar)

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

    paginator_links_pref = "/?order_by=%s&order_dir=%s&psize=%s" % (order_by, order_dir, page_size)
    psize_select_pref = "/?order_by=%s&order_dir=%s&page=%s" % (order_by, order_dir, page)

    page_link_lower = page - 5
    page_link_upper = page + 5

    # --- Links del header ---

    link_col_ficha = get_sort_link('id', order_by, order_dir, page, page_size)
    link_col_centro = get_sort_link('centro_familiar', order_by, order_dir, page, page_size)
    link_col_apellidos = get_sort_link('apellidos', order_by, order_dir, page, page_size)
    link_col_tipo = get_sort_link('tipo_de_familia', order_by, order_dir, page, page_size)
    link_col_estado = get_sort_link('estado', order_by, order_dir, page, page_size)

    return render(request, 'home.html', locals())


@login_required
def familia(request, id):
    id = int(id)
    message = None
    message_class = ''
    es_admin = request.user.is_superuser

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
            message = DATOS_GUARDADOS
            message_class = 'success'
            if id == 0:
                return HttpResponseRedirect('/familia/%s' % familia_form.instance.id)
    else:
        if familia is not None:
            familia_form = FamiliaForm(instance=familia)
        else:
            # agregar nuevo registro
            user_profile = request.user.get_profile()
            centro = user_profile.centro_familiar.id if user_profile.centro_familiar is not None else None
            familia_form = FamiliaForm(initial={'centro_familiar': centro})

    return render(request, 'ficha_familia.html', locals())


@login_required
def eliminar_familia(request, id):

    if request.method == 'POST':
        id = request.POST['id']

    try:
        familia = Familia.objects.get(id=id)
    except:
        return Http404()

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
        return Http404()

    if request.method == 'POST':
        persona.delete()
        return HttpResponseRedirect(next)

    return render(request, 'eliminar_persona.html', locals())


@login_required
def get_persona_form(request, familia_id, id):

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


@login_required
def ficha(request, id):
    try:
        persona = Persona.objects.get(id=id)
    except:
        return Http404()
    form = EvaluacionForm(initial={'persona': persona})
    return render(request, 'ficha_persona.html', locals())
