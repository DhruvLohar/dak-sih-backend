from django.contrib import admin
from .models import *
from django.utils.html import format_html

class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active', 'likes_count', 'content_excerpt')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'content', 'likes_count', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def content_excerpt(self, obj):
        return format_html('<p>{}</p>', obj.content[:50] + '...')  # Show an excerpt of the content
    content_excerpt.short_description = 'Content'

class ForumPostReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('post', 'user', 'content', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(ForumPostReply, ForumPostReplyAdmin)
