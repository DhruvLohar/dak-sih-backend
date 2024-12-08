from django.contrib import admin
from .models import *

# TODO: Register models for PostalOffice and AdminUser
@admin.register(PostalOffice)
class PostalOfficeAdmin(admin.ModelAdmin):
    list_display = ['alias', 'main_office', 'sub_division', 'postal_code']

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'postal_office', 'is_super_admin']

@admin.register(PDA)
class PDAApplicationAdmin(admin.ModelAdmin):
    list_display = ['name_of_applicant', 'date_of_application', 'status']


