from rest_framework import serializers
from .models import (Product, Productdiscount, productImage, Seller, Attrar,
                     AttrarName, Category, Brand, GeneralSpecifications, SpecificationsValue)
import locale
locale.setlocale(locale.LC_ALL, '')


class specificationsValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationsValue
        fields = '__all__'


class generalspecificationsser(serializers.ModelSerializer):
    specificationsvalue_set = specificationsValueSerializer(many=True)

    class Meta:
        model = GeneralSpecifications
        fields = '__all__'


class discountser(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    discountdate = serializers.SerializerMethodField()
    Percentage = serializers.SerializerMethodField()
    pricenumber = serializers.SerializerMethodField()

    def get_discount(self, obj):
        price1 = (obj.productdiscount.discount_percent * obj.primary_price) / 100
        price1 = obj.primary_price - price1
        return f'{int(price1):n}'

    def get_discountdate(self, obj):
        return obj.productdiscount.data_status

    def get_Percentage(self, obj):
        return str(obj.productdiscount.discount_percent)

    def get_pricenumber(self, obj):
        return f'{obj.primary_price:n}'

    class Meta:
        model = Product
        exclude = ('eng_name', 'description', 'publish_date', 'suggest', 'primary_price')


class imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productImage
        exclude = ('product',)


class search_ser(serializers.ModelSerializer):
    catname = serializers.SerializerMethodField()

    def get_catname(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = ('description', 'publish_date', 'primary_price', 'primary_image',
                   'discount_status', 'suggest', 'seller', 'productdiscount',)


class sellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        exclude = ('id', )


class attrarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attrar
        fields = '__all__'


class attrSerializer(serializers.ModelSerializer):
    attrar_set = attrarSerializer(many=True)

    class Meta:
        model = AttrarName
        fields = '__all__'


class generalspecificSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralSpecifications
        fields = '__all__'


class specificValueSerializer(serializers.ModelSerializer):
    generalspecifications = generalspecificSerializer()

    class Meta:
        model = SpecificationsValue
        fields = '__all__'


class productser(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    discountdate = serializers.SerializerMethodField()
    Percentage = serializers.SerializerMethodField()
    pricenumber = serializers.SerializerMethodField()
    catname = serializers.SerializerMethodField()
    brandname = serializers.SerializerMethodField()
    items = imageSerializer(many=True)
    seller = sellerSerializer(many=True)
    attrarname_set = attrSerializer(many=True)
    specificationsvalue = specificValueSerializer(many=True)

    def get_catname(self, obj):
        return obj.category.name

    def get_brandname(self, obj):
        return obj.brand.name

    def get_discount(self, obj):
        price1 = (obj.productdiscount.discount_percent * obj.primary_price) / 100
        price1 = obj.primary_price - price1
        return f'{int(price1):n}'

    def get_discountdate(self, obj):
        return obj.productdiscount.data_status

    def get_Percentage(self, obj):
        return str(obj.productdiscount.discount_percent)

    def get_pricenumber(self, obj):
        return f'{obj.primary_price:n}'

    class Meta:
        model = Product
        exclude = ('primary_price',)


class catser(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class brandser(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class sellerser(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class productserilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class catchildser(serializers.ModelSerializer):
    subname = serializers.SerializerMethodField()

    def get_subname(self, obj):
        return obj.parent.name

    class Meta:
        model = Category
        fields = '__all__'
