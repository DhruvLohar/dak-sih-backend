from django.contrib import admin
from .models import Philatelist

from django.utils.html import format_html

@admin.register(Philatelist)
class PhilatelistAdmin(admin.ModelAdmin):
    
    readonly_fields = ('id', 'access_token', 'created_at', 'modified_at',)
    
    fieldsets = (
        (None, {'fields': ('id', 'is_active', 'valid_otp',)}),
        ('Personal Information', {
            'fields': ('profile_img', 'name', 'phone_number', 'email', 'gender',)
        }),
        ('Address', {
            'fields': ('address', 'postal_code',)
        }),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'modified_at',)}),
        ('User Tokens', {'fields': ('access_token',)}),
    )
    
    def copy_access_token(self, obj):
        return format_html(
            '<button onclick="navigator.clipboard.writeText(\'{0}\').then(() => alert(\'Access Token copied to clipboard\'))">Copy</button>',
            obj.access_token
        )
        
    list_display = ['id', 'name', 'phone_number', 'copy_access_token']