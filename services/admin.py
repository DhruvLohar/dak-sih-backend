from django.contrib import admin
from .models import *

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['slug', 'published_date']
    list_filter = ['published_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['published_date']
    
    fieldsets = (
        ('General Information', {
            'fields': ('slug', 'title', 'description', 'published_date', 'read_time')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at',)
    
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at',)

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'coining_date', 'quantity_produced', 'created_at')
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "image"),
        }),
        ("Details", {
            "fields": ("coining_date", "backstory", "quantity_produced"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "modified_at"),
            "classes": ("collapse",),
        }),
    )  
    
    readonly_fields = ('created_at', 'modified_at')
