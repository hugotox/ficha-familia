# -*- encoding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from mensajes import DATOS_GUARDADOS, FORM_INCORRECTO, CERRAR_CICLO
from main.models import *
from django.utils import simplejson
from django.core import serializers
from utils.json_utils import json_response


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
    familias = Familia.objects.select_related('persona', 'estadofamiliaanio')
    centros = CentroFamiliar.objects.all().order_by('comuna')
    tipos = TIPOS_FAMILIA_CHOICES
    estados = ESTADO_FAMILIA_CHOICES
    user_profile = request.user.get_profile()
    tipo_registro = 'Familias'

    # --- Filtros ---
    num_ficha = request.GET.get('num_ficha', '')
    centro = request.GET.get('centro', '')
    apellidos = request.GET.get('apellidos', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    anio = int(request.GET.get('anio', datetime.now().year))

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
        the_aps = apellidos.split(' ')
        for ap in the_aps:
            familias = familias.filter(
                Q(apellido_paterno__icontains=ap) |
                Q(apellido_materno__icontains=ap) |
                Q(persona__apellido_paterno__icontains=ap) |
                Q(persona__apellido_materno__icontains=ap) |
                Q(persona__nombres__icontains=ap)
            )

    if tipo != '':
        familias = familias.filter(tipo_de_familia=tipo)

    if estado != '':

        if estado == 'Inactivo':
            familias = familias.filter(estadofamiliaanio__anio=anio, estadofamiliaanio__inactivo=True)
        elif estado == 'Activo':
            familias = familias.filter(estadofamiliaanio__anio=anio, estadofamiliaanio__activo=True)
        elif estado == 'Completo':
            familias = familias.filter(estadofamiliaanio__anio=anio, estadofamiliaanio__completo=True)

    familias = familias.distinct()

    filtros_params = 'num_ficha=%s&centro=%s&apellidos=%s&tipo=%s&estado=%s' % (num_ficha, centro, apellidos, tipo, estado)

    # --- Orden ---
    columnas_permitidas = ['id', 'centro_familiar', 'apellidos', 'tipo_de_familia', 'estado']
    order_by = request.GET.get('order_by', 'apellidos')
    if order_by not in columnas_permitidas:
        order_by = 'apellidos'
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
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        familias = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    paginator_links_pref = "/?order_by=%s&order_dir=%s&psize=%s&%s" % (order_by, order_dir, page_size, filtros_params)
    psize_select_pref = "/?order_by=%s&order_dir=%s&page=%s&%s" % (order_by, order_dir, page, filtros_params)

    page_link_lower = page - 5
    page_link_upper = page + 5

    # --- Links del header ---

    link_col_ficha = get_sort_link('id', order_by, order_dir, page, page_size, filtros_params)
    link_col_centro = get_sort_link('centro_familiar', order_by, order_dir, page, page_size, filtros_params)
    link_col_apellidos = get_sort_link('apellidos', order_by, order_dir, page, page_size, filtros_params)
    link_col_tipo = get_sort_link('tipo_de_familia', order_by, order_dir, page, page_size, filtros_params)
    link_col_estado = get_sort_link('estado', order_by, order_dir, page, page_size, filtros_params)

    current_querystring = "order_by=%s&order_dir=%s&page=%s&psize=%s&%s&anio=%s" % (order_by, order_dir, page, page_size, filtros_params, anio)

    return render(request, 'home.html', locals())


@login_required
def familia(request, id):
    id = int(id)
    message = None
    message_class = ''
    user_profile = request.user.get_profile()
    es_admin = request.user.is_superuser
    centro_familiar = None
    current_year = datetime.now().year

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

    if not es_admin and familia is not None:
        if familia.centro_familiar != centro_familiar:
            raise Http404

    if request.method == "POST":
        anio = request.POST.get('anio', current_year)

        if familia is not None:
            familia_form = FamiliaForm(request.POST, instance=familia)
        else:
            familia_form = FamiliaForm(request.POST)  # post de una nueva

        if familia_form.is_valid():
            familia_form.save()
            # familia_form.instance.actualizar_estado()
            message = DATOS_GUARDADOS
            message_class = 'success'

            # guardar "aporta" en objeto persona
            for persona in familia_form.instance.persona_set.all():
                aporta = request.POST.get('aporta-%s' % persona.id)
                persona.aporta_ingreso = aporta == u'Sí'
                persona.save()

            if id == 0:
                request.session['nueva_familia'] = True
                return HttpResponseRedirect('/familia/%s%s' % (familia_form.instance.id, back_url))

        else:
            message_class = "error"
            message = FORM_INCORRECTO
    else:
        anio = current_year
        if familia is not None:
            estado, c = EstadoFamiliaAnio.objects.get_or_create(familia=familia, anio=anio)
            familia_form = FamiliaForm(instance=familia, initial={
                'cond_precariedad': estado.cond_precariedad,
                'cond_precariedad_coment': estado.cond_precariedad_coment,
                'cond_vulnerabilidad': estado.cond_vulnerabilidad,
                'cond_vulnerabilidad_coment': estado.cond_vulnerabilidad_coment,
                'cond_hogar_uni_riesgo': estado.cond_hogar_uni_riesgo,
                'cond_hogar_uni_riesgo_coment': estado.cond_hogar_uni_riesgo_coment,
                'cond_familia_mono_riesgo': estado.cond_familia_mono_riesgo,
                'cond_familia_mono_riesgo_coment': estado.cond_familia_mono_riesgo_coment,
                'cond_alcohol_drogas': estado.cond_alcohol_drogas,
                'cond_alcohol_drogas_coment': estado.cond_alcohol_drogas_coment,
                'cond_discapacidad': estado.cond_discapacidad,
                'cond_discapacidad_coment': estado.cond_discapacidad_coment,
                'cond_malos_tratos': estado.cond_malos_tratos,
                'cond_malos_tratos_coment': estado.cond_malos_tratos_coment,
                'cond_socializ_delictual': estado.cond_socializ_delictual,
                'cond_socializ_delictual_coment': estado.cond_socializ_delictual_coment,
            })
        else:
            # agregar nuevo registro
            centro = user_profile.centro_familiar.id if user_profile.centro_familiar is not None else None
            familia_form = FamiliaForm(initial={'centro_familiar': centro})

        if request.session.get('nueva_familia', False):
            message = DATOS_GUARDADOS
            message_class = 'success'
            request.session['nueva_familia'] = False

    anios = range(2013, datetime.now().year+1)

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
        if persona.fecha_nacimiento == settings.NULL_DATE:
            persona.fecha_nacimiento = None
            persona.save()

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


def crear_listas_objetivos(obj_qs):
    daList = []
    for obj in obj_qs:
        daList.append({
            'evaluacion': obj.evaluacion.id,
            'factor': obj.factor.id,
            'tipo': obj.tipo,
            'componente': obj.factor.componente.id
        })
    return daList


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
    objetivos_ind_qs = simplejson.dumps([])
    objetivos_grup_qs = simplejson.dumps([])

    evaluacion_qs = EvaluacionFactoresProtectores.objects.filter(persona=persona, anio_aplicacion=anio)

    cerrar_ciclo_label = CERRAR_CICLO

    if evaluacion_qs.count():
        evaluacion = evaluacion_qs[0]

    # existe la evaluacion anio anterior?
    show_previous_ev_btn = EvaluacionFactoresProtectores.objects.filter(
        persona=persona, anio_aplicacion=datetime.now().year - 1, ciclo_cerrado=True)\
        .count() == 1

    if request.method == "POST":
        action = request.POST.get('action', 'Guardar')

        tab = 2

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

                if int(form_anio) < 2013:
                    message = u"Por favor ingrese un año igual o mayor a 2013."
                    message_class = "error"
                    valid = False

                elif EvaluacionFactoresProtectores.objects.filter(persona=persona, anio_aplicacion=form_anio).count():
                    message = "La ficha para esta persona/año ya existe. Por favor vuelva a la página anterior y 1) Seleccione la ficha existente o 2) Cree una nueva ficha para un año diferente."
                    message_class = "error"
                    valid = False

            if valid:

                # guarda el registro evaluacion
                form.save()

                # guarda los objetivos por componente
                comp_ind_list = request.POST.getlist('componente-ind')
                comp_grup_list = request.POST.getlist('componente-grup')
                objetivo_ind_list = request.POST.getlist('objetivo-ind')
                objetivo_grup_list = request.POST.getlist('objetivo-grup')

                eval_instance = form.instance

                eval_instance.objetivosevaluacion_set.all().delete()

                agregados = []

                i = 0
                for comp_ind in comp_ind_list:
                    if comp_ind != '':
                        if len(objetivo_ind_list) > i:
                            obj_ind = objetivo_ind_list[i]
                            if obj_ind != '':
                                if (comp_ind, obj_ind) not in agregados:
                                    oFactor = FactorProtector.objects.get(pk=obj_ind)
                                    oObjetivo = ObjetivosEvaluacion(evaluacion=eval_instance, factor=oFactor, tipo=1)
                                    oObjetivo.save()
                                    agregados.append((comp_ind, obj_ind))
                    i += 1

                agregados = []
                i = 0
                for comp_grup in comp_grup_list:
                    if comp_grup != '':
                        if len(objetivo_grup_list) > i:
                            obj_grup = objetivo_grup_list[i]
                            if obj_grup != '':
                                if (comp_grup, obj_grup) not in agregados:
                                    oFactor = FactorProtector.objects.get(pk=obj_grup)
                                    oObjetivo = ObjetivosEvaluacion(evaluacion=eval_instance, factor=oFactor, tipo=2)
                                    oObjetivo.save()
                                    agregados.append((comp_grup, obj_grup))
                    i += 1

                # actualizar el estado de la familia
                if str(anio) == '0':
                    form_anio = int(form.cleaned_data['anio_aplicacion'])
                else:
                    form_anio = int(anio)
                persona.familia.actualizar_estado(form_anio)

                if evaluacion is None:
                    return HttpResponseRedirect("/ficha/%s/%s/?%s" % (persona.id, form.instance.anio_aplicacion, str_filters))

                # re-crear el form para q se muestren los cambios
                form = EvaluacionForm(instance=form.instance)
                objetivos_ind_qs = simplejson.dumps(crear_listas_objetivos(eval_instance.objetivosevaluacion_set.filter(tipo=1)))
                objetivos_grup_qs = simplejson.dumps(crear_listas_objetivos(eval_instance.objetivosevaluacion_set.filter(tipo=2)))

                if action == CERRAR_CICLO:
                    return HttpResponseRedirect("/ficha/%d/%s/cerrar/?%s" % (persona.id, evaluacion.anio_aplicacion, str_filters))

        else:
            message_class = "error"
            message = FORM_INCORRECTO

        # elif action == 'Cerrar Ciclo':
        #     message = evaluacion.cerrar_ciclo()
        #     if message == "":  # exito
        #         message_class = "success"
        #         message = "Se ha cerrado esta ficha correctamente."
        #     else:  # error
        #         message_class = "error"
        #
        #     tab = 1
        #     form = EvaluacionForm(instance=evaluacion)
        #     objetivos_ind_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=1)))
        #     objetivos_grup_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=2)))

    else:  # GET handler
        tab = 1
        if evaluacion is not None:
            # existe
            form = EvaluacionForm(instance=evaluacion)
            objetivos_ind_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=1)))
            objetivos_grup_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=2)))

            if 'message_class_cerrar' in request.session and 'message_cerrar' in request.session:
                message_class = request.session['message_class_cerrar']
                message = request.session['message_cerrar']
                request.session['message_class_cerrar'] = ''
                request.session['message_cerrar'] = ''

        else:
            # nueva
            form = EvaluacionForm(initial={'persona': persona, 'anio_aplicacion': datetime.now().year})

    return render(request, 'ficha_persona.html', locals())


@login_required
def cerrar_ciclo(request, id, anio):
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
        message = evaluacion.cerrar_ciclo()
        if message == "":  # exito
            request.session['message_class_cerrar'] = "success"
            request.session['message_cerrar'] = "Se ha cerrado esta ficha correctamente."
        else:  # error
            request.session['message_class_cerrar'] = "error"
            request.session['message_cerrar'] = message

        tab = 1
        form = EvaluacionForm(instance=evaluacion)
        objetivos_ind_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=1)))
        objetivos_grup_qs = simplejson.dumps(crear_listas_objetivos(evaluacion.objetivosevaluacion_set.filter(tipo=2)))

        # /ficha/{{ persona.id }}/{{ eval.anio_aplicacion }}{{ back_url }}
        return HttpResponseRedirect("/ficha/%s/%s/?%s" % (persona.id, evaluacion.anio_aplicacion, "&".join(filters)))

    return render(request, 'cerrar_ciclo.html', locals())



@login_required
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
        evaluacion.persona.familia.actualizar_estado(anio)
        evaluacion.delete()
        return HttpResponseRedirect("/familia/%s/?%s" % (persona.familia.id, "&".join(filters)))

    return render(request, 'eliminar_ficha.html', locals())


@login_required
def get_detalle_familia(request, id):
    familia = Familia.objects.get(id=id)
    html = render_to_string("tabla_personas_home.html", locals())
    return HttpResponse(html, content_type='text/plain')


@login_required
def update_aporta(request):
    success = False
    if request.method == "POST":
        persona_id = request.POST.get('persona_id', None)
        value = request.POST.get('value', 'No')
        try:
            persona = Persona.objects.get(id=persona_id)
            persona.aporta_ingreso = value == u'Sí'
            persona.save()
            success = True
        except:
            pass

    if success:
        return json_response({'success': True, 'msg': 'Saved'})
    else:
        return json_response({'success': False, 'msg': 'Operation not allowed'})


@login_required
def copiar_datos_anterior(request, id_persona):
    try:
        persona = Persona.objects.get(id=id_persona)
        eva_anterior = EvaluacionFactoresProtectores.objects.get(persona=persona, anio_aplicacion=datetime.now().year - 1, ciclo_cerrado=True)
    except:
        return json_response({'success': False})

    return json_response({'success': True, 'data': {
        'presencia_red_de_apoyo': eva_anterior.presencia_red_de_apoyo2,
        'relaciones_con_vecindario': eva_anterior.relaciones_con_vecindario2,
        'participacion_social': eva_anterior.participacion_social2,
        'red_de_servicios_y_beneficios_sociales': eva_anterior.red_de_servicios_y_beneficios_sociales2,
        'ocio_y_encuentro_con_pares': eva_anterior.ocio_y_encuentro_con_pares2,
        'espacios_formativos_y_de_desarrollo': eva_anterior.espacios_formativos_y_de_desarrollo2,
        'relaciones_y_cohesion_familiar': eva_anterior.relaciones_y_cohesion_familiar2,
        'adaptabilidad_y_resistencia_familiar': eva_anterior.adaptabilidad_y_resistencia_familiar2,
        'competencias_parentales': eva_anterior.competencias_parentales2,
        'proteccion_y_salud_integral': eva_anterior.proteccion_y_salud_integral2,
        'participacion_protagonica': eva_anterior.participacion_protagonica2,
        'recreacion_y_juego_con_pares': eva_anterior.recreacion_y_juego_con_pares2,
        'crecimiento_personal': eva_anterior.crecimiento_personal2,
        'autonomia': eva_anterior.autonomia2,
        'habilidades_y_valores_sociales': eva_anterior.habilidades_y_valores_sociales2
    }})


@login_required
def get_condiciones_familia(request, id, anio):
    try:
        familia = Familia.objects.get(id=id)
        estado = EstadoFamiliaAnio.objects.get(familia=familia, anio=anio)
    except:
        return json_response({'success': False})

    return json_response({
        'success': True,
        'data': {
            'cond_precariedad': estado.cond_precariedad,
            'cond_precariedad_coment': estado.cond_precariedad_coment,
            'cond_vulnerabilidad': estado.cond_vulnerabilidad,
            'cond_vulnerabilidad_coment': estado.cond_vulnerabilidad_coment,
            'cond_hogar_uni_riesgo': estado.cond_hogar_uni_riesgo,
            'cond_hogar_uni_riesgo_coment': estado.cond_hogar_uni_riesgo_coment,
            'cond_familia_mono_riesgo': estado.cond_familia_mono_riesgo,
            'cond_familia_mono_riesgo_coment': estado.cond_familia_mono_riesgo_coment,
            'cond_alcohol_drogas': estado.cond_alcohol_drogas,
            'cond_alcohol_drogas_coment': estado.cond_alcohol_drogas_coment,
            'cond_discapacidad': estado.cond_discapacidad,
            'cond_discapacidad_coment': estado.cond_discapacidad_coment,
            'cond_malos_tratos': estado.cond_malos_tratos,
            'cond_malos_tratos_coment': estado.cond_malos_tratos_coment,
            'cond_socializ_delictual': estado.cond_socializ_delictual,
            'cond_socializ_delictual_coment': estado.cond_socializ_delictual_coment,
        }
    })