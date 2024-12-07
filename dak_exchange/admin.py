# TODO: Add admin support for ExchangeProduct and ExchangeOrder
from django.contrib import admin
from .models import *

@admin.register(ExchangeProduct)
class ExchangeProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'current_owner', 'quantity', 'quantity_sold', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = [
        (None, {'fields': ['slug', 'title', 'description', 'details', 'price', 'quantity']}),
        ('Ownership', {'fields': ['current_owner', 'previous_owners']}),
        ('Status', {'fields': ['is_active']}),
        ('Dates', {'fields': ['created_at', 'updated_at']}),
    ]

    readonly_fields = ['current_owner', 'previous_owners', 'quantity_sold', 'is_active', 'created_at', 'updated_at']
    
    class ExchangeProductImageInline(admin.TabularInline):
        model = ExchangeProductImage
        extra = 1
        
    inlines = [ExchangeProductImageInline]

@admin.register(ExchangeOrder)
class ExchangeOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'status', 'created_at']
    
    fieldsets = [
        (None, {'fields': ['user', 'product', 'status']}),
        ('Transaction Details', {'fields': ['transaction_details']}),
        ('Dates', {'fields': ['created_at', 'updated_at']}),
    ]
    
    readonly_fields = ['user', 'product', 'status', 'created_at', 'updated_at']

