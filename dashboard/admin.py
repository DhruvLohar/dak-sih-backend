from django.contrib import admin
from .models import PostalOffice, AdminUser

# TODO: Register models for PostalOffice and AdminUser
@admin.register(PostalOffice)
class PostalOfficeAdmin(admin.ModelAdmin):
    list_display = ['alias', 'main_office', 'sub_division', 'postal_code']

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'postal_office']

