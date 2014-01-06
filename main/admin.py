from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class EvalAdmin(admin.ModelAdmin):
    search_fields = ('persona__apellido_paterno', 'persona__apellido_materno',
                     'persona__familia__apellido_paterno', 'persona__familia__apellido_materno',
                     'persona__familia__centro_familiar__comuna')
    list_display = ('anio_aplicacion', 'persona', 'get_familia', 'get_centrofamiliar')


class FamiliasAdmin(admin.ModelAdmin):
    search_fields = ('apellido_paterno', 'apellido_materno')


class PersonasAdmin(admin.ModelAdmin):
    search_fields = ('apellido_paterno', 'apellido_materno',)


admin.site.register(Familia, FamiliasAdmin)
admin.site.register(CentroFamiliar)
admin.site.register(Persona, PersonasAdmin)
admin.site.register(EvaluacionFactoresProtectores, EvalAdmin)
#admin.site.register(UserProfile)
admin.site.register(Componentes)
admin.site.register(FactorProtector)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)