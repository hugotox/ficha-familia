from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^familia/(?P<id>\d+)/$', 'main.views.familia', name='familia'),
    url(r'^familia/(?P<id>\d+)/del/$', 'main.views.eliminar_familia', name='eliminar_familia'),
    url(r'^ficha/(?P<id>\d+)/(?P<anio>\d+)/$', 'main.views.ficha', name='ficha'),
    url(r'^ficha/(?P<id>\d+)/(?P<anio>\d+)/del/$', 'main.views.eliminar_ficha', name='eliminar_ficha'),
    url(r'^persona/del/(?P<id>\d+)/$', 'main.views.eliminar_persona', name='eliminar_persona'),
    url(r'^get_persona_form/(?P<familia_id>\d+)/(?P<id>\d+)$', 'main.views.get_persona_form', name='get_persona_form'),
    url(r'^accounts/login/$', 'main.auth.login_view', name='login'),
    url(r'^accounts/logout/$', 'main.auth.logout_view', name='logout'),
    url(r'^get_objetivos/(?P<alcance>\w+)/(?P<comp_id>\d+)/', 'main.views.get_objetivos'),
)
