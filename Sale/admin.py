from django.contrib import admin
from .models import Cart, ProductCart


class ProductCartAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'user',
        'cart',
    )
    search_fields = ('product', 'user', 'cart')
    list_filter = ('quantity', 'cart',)


admin.site.register(ProductCart, ProductCartAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'publish_date',
        'status',
    )
    search_fields = ('user',)
    list_filter = ('publish_date', 'status',)


admin.site.register(Cart, CartAdmin)
