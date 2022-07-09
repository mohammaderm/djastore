from rest_framework import serializers
from .models import ProductCart


class ProductCartserializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_img = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    def get_product_img(self, obj):
        return obj.product.primary_image.url

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_price(self, obj):
        return obj.product.primary_price

    class Meta:
        model = ProductCart
        fields = '__all__'
