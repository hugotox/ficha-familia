from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Familia)
admin.site.register(CentroFamiliar)
admin.site.register(Persona)
admin.site.register(EvaluacionFactoresProtectores)
admin.site.register(UserProfile)


# No funciona!
#
# # Define an inline admin descriptor for UserProfile model
# # which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'profile'
#
# # Define a new User admin
# class UserAdmin(UserAdmin):
#     inlines = (UserProfileInline, )
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)