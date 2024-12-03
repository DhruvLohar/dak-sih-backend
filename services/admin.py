from django.contrib import admin
from .models import *

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at',)
    
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at',)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description', 'address', 'tags')
    readonly_fields = ('created_at', 'modified_at')
    ordering = ('-date',)

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "banner", "tags"),
        }),
        ("Schedule & Location", {
            "fields": ("date", "duration", "address"),
        }),
        ("Pricing", {
            "fields": ("price",),
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "modified_at"),
            "classes": ("collapse",),  # Collapsible section for timestamps
        }),
    )

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
