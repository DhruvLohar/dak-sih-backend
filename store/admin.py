from django.contrib import admin
from .models import *

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'title': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'quantity_sold', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'collection')
    search_fields = ('title', 'description')
    prepopulated_fields = {'title': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'quantity', 'quantity_sold', 'is_active')
        }),
        ('Relations and Metadata', {
            'fields': ('collection', 'current_state'),
        }),
    )

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__name', 'product__title', 'review')
    fieldsets = (
        ('Review Details', {
            'fields': ('product', 'user', 'rating', 'review'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('id', 'user__name')
    fieldsets = (
        ('Order Details', {
            'fields': ('user', 'status')
        }),
    )


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('order__id', 'product__title')
