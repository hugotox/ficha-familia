from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'main.views.home', name='home'),
   url(r'^accounts/login/$', 'main.auth.login_view', name='login'),
   url(r'^accounts/logout/$', 'main.auth.logout_view', name='logout'),

)
