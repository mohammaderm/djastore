from rest_framework import serializers
from .models import Cumment, Like, Bookmark


class CummentSerialzer(serializers.ModelSerializer):
    userfullname = serializers.SerializerMethodField()

    def get_userfullname(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)

    class Meta:
        model = Cumment
        fields = '__all__'


class Likeserializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_name_eng = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    cat_name = serializers.SerializerMethodField()
    product_img = serializers.SerializerMethodField()
    catid = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_name_eng(self, obj):
        return obj.product.eng_name

    def get_cat_name(self, obj):
        return obj.product.category.name

    def get_catid(self, obj):
        return obj.product.category.id

    def get_product_price(self, obj):
        return obj.product.primary_price

    def get_product_img(self, obj):
        return obj.product.primary_image.url

    class Meta:
        model = Like
        fields = '__all__'


class bookmarkserializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_name_eng = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    cat_name = serializers.SerializerMethodField()
    product_img = serializers.SerializerMethodField()
    catid = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_name_eng(self, obj):
        return obj.product.eng_name

    def get_cat_name(self, obj):
        return obj.product.category.name

    def get_catid(self, obj):
        return obj.product.category.id

    def get_product_price(self, obj):
        return obj.product.primary_price

    def get_product_img(self, obj):
        return obj.product.primary_image.url

    class Meta:
        model = Bookmark
        fields = '__all__'


class cummentuserserializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    class Meta:
        model = Cumment
        fields = '__all__'
