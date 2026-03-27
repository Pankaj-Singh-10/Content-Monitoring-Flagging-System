from django.contrib import admin
from .models import Keyword, ContentItem, Flag


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'last_updated', 'created_at']
    list_filter = ['source']
    search_fields = ['title', 'body']
    date_hierarchy = 'last_updated'


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'content_item', 'score', 'status', 'created_at']
    list_filter = ['status', 'score']
    search_fields = ['keyword__name', 'content_item__title']
    readonly_fields = ['created_at', 'updated_at']

    