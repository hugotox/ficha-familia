from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^familia/(?P<id>\d+)/$', 'main.views.familia', name='familia'),
    url(r'^get_detalle_familia/(?P<id>\d+)/$', 'main.views.get_detalle_familia', name='get_detalle_familia'),
    url(r'^familia/(?P<id>\d+)/del/$', 'main.views.eliminar_familia', name='eliminar_familia'),
    url(r'^ficha/(?P<id>\d+)/(?P<anio>\d+)/$', 'main.views.ficha', name='ficha'),
    url(r'^ficha/(?P<id>\d+)/(?P<anio>\d+)/del/$', 'main.views.eliminar_ficha', name='eliminar_ficha'),
    url(r'^ficha/(?P<id>\d+)/(?P<anio>\d+)/cerrar/$', 'main.views.cerrar_ciclo', name='cerrar_ciclo'),
    url(r'^ficha/(?P<id_persona>\d+)/copiar/$', 'main.views.copiar_datos_anterior', name='copiar_datos_anterior'),
    url(r'^persona/del/(?P<id>\d+)/$', 'main.views.eliminar_persona', name='eliminar_persona'),
    url(r'^persona/update_aporta/$', 'main.views.update_aporta', name='update_aporta'),
    url(r'^get_persona_form/(?P<familia_id>\d+)/(?P<id>\d+)$', 'main.views.get_persona_form', name='get_persona_form'),
    url(r'^accounts/login/$', 'main.auth.login_view', name='login'),
    url(r'^accounts/logout/$', 'main.auth.logout_view', name='logout'),
    url(r'^accounts/changepasswd/$', 'django.contrib.auth.views.password_change', {'template_name': 'changepasswd.html'}, name='changepasswd'),
    url(r'^accounts/changepasswd/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'changepasswd_done.html'}, name='changepasswd_done'),

    #reportes
    url(r'^reportes/$', 'main.reports_views.home', name='home_reports'),
    url(r'^reportes/(?P<anio>\d+)/$', 'main.reports_views.home', name='home_reports'),
    url(r'^reportes/(?P<anio>\d+)/cantidad_fichas/$', 'main.reports_views.home', name='home_reports'),
    url(r'^reportes/(?P<anio>\d+)/cantidad_fichas/(?P<tipo>\w+)/$', 'main.reports_views.cantidad_fichas', name='cantidad_fichas'),
    url(r'^reportes/(?P<anio>\d+)/tipos_familias/$', 'main.reports_views.tipos_familias', name='tipos_familias'),
    url(r'^reportes/(?P<anio>\d+)/estado_ciclos/$', 'main.reports_views.estado_ciclos', name='estado_ciclos'),
    url(r'^reportes/(?P<anio>\d+)/estado_datos/$', 'main.reports_views.estado_datos', name='estado_datos'),
    url(r'^reportes/(?P<anio>\d+)/rel_familia_persona/$', 'main.reports_views.rel_familia_persona', name='rel_familia_persona'),
    url(r'^reportes/(?P<anio>\d+)/fichas_por_objetivo/$', 'main.reports_views.fichas_por_objetivo', name='fichas_por_objetivo'),
    url(r'^reportes/(?P<anio>\d+)/fichas_por_objetivo_comuna/((?P<factor_id>\d+))/$', 'main.reports_views.fichas_por_objetivo_comuna', name='fichas_por_objetivo_comuna'),
    url(r'^reportes/(?P<anio>\d+)/condiciones_vulnerabilidad/$', 'main.reports_views.condiciones_vulnerabilidad', name='condiciones_vulnerabilidad'),
    url(r'^reportes/(?P<anio>\d+)/participacion_actividades/$', 'main.reports_views.participacion_actividades', name='participacion_actividades'),
    url(r'^reportes/(?P<anio>\d+)/actividades_objetivo/$', 'main.reports_views.actividades_objetivo', name='actividades_objetivo'),
    url(r'^reportes/(?P<anio>\d+)/var_por_factor/$', 'main.reports_views.prom_por_factor', name='prom_por_factor'),
    url(r'^reportes/(?P<anio>\d+)/var_por_obj/$', 'main.reports_views.var_por_obj', name='var_por_obj'),
)
