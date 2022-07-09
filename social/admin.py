from django.contrib import admin
from .models import Bookmark, Cumment, Like


class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
    )
    search_fields = ('user', 'product')
    list_filter = ('user', 'product',)


admin.site.register(Bookmark, BookmarkAdmin)


class CummentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'value',
        'product',
        'publish_date',
        'validation',
    )
    search_fields = ('user', 'product')
    list_filter = ('publish_date', 'validation',)


admin.site.register(Cumment, CummentAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
    )
    search_fields = ('user', 'product')
    list_filter = ('user', 'product',)


admin.site.register(Like, LikeAdmin)
