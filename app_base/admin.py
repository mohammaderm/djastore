from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import (Seller, Product, productImage, Productdiscount, Category,
                     AttrarName, Attrar, Brand, GeneralSpecifications, SpecificationsValue)

admin.site.register(Seller)
admin.site.register(productImage)
admin.site.register(Productdiscount)
admin.site.register(Brand)
admin.site.register(SpecificationsValue)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'parent',
    )
    search_fields = ('name',)
    list_filter = ('parent',)


admin.site.register(Category, CategoryAdmin)


class productImageInline(NestedStackedInline):
    model = productImage
    extra = 1
    fk_name = 'product'


class SpecificationsValueInline(NestedStackedInline):
    model = SpecificationsValue
    extra = 1
    fk_name = 'generalspecifications'


class GeneralSpecificationsAdmin(NestedModelAdmin):
    model = GeneralSpecifications
    inlines = [SpecificationsValueInline]


admin.site.register(GeneralSpecifications, GeneralSpecificationsAdmin)


class AttrarInline(NestedStackedInline):
    model = Attrar
    extra = 1
    fk_name = 'attrarname'


class AttrarNameInline(NestedStackedInline):
    model = AttrarName
    extra = 1
    fk_name = 'product'
    inlines = [AttrarInline]


class ProductAdmin(NestedModelAdmin):
    model = Product
    inlines = [AttrarNameInline, productImageInline]
    list_display = (
        'name',
        'category',
        'brand',
        'primary_price',
    )
    search_fields = ('name', 'category', 'brand',)
    list_filter = ('category', 'brand',)


admin.site.register(Product, ProductAdmin)
