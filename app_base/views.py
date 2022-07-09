from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Product, Category, Brand, Seller, GeneralSpecifications
from rest_framework.response import Response
from rest_framework import status
from .serializer import (discountser, productser, catser, search_ser, productserilizer,
                         brandser, sellerser, generalspecificationsser, catchildser)
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
import collections


class Search_product(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = search_ser
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'eng_name', 'category__name']


class Get_product_in_category(ListAPIView):
    serializer_class = discountser
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand_id', 'seller', 'specificationsvalue']

    def get_queryset(self):
        obj_id = self.request.GET.get("id")
        brand_list = self.request.GET.getlist("brand")
        seller_list = self.request.GET.getlist("seller")
        specif_list = self.request.GET.getlist("specificationsvalue")
        general_list = self.request.GET.getlist("generalspecifications")
        if brand_list:
            return Product.objects.filter(Q(Q(category=obj_id) | Q(
                category__parent=obj_id)) & Q(brand__in=brand_list))

        elif seller_list:
            return Product.objects.filter(Q(
                Q(category=obj_id) | Q(category__parent=obj_id)) & Q(
                seller__in=seller_list))

        elif specif_list and general_list:
            obj = Product.objects.filter(Q(category=obj_id) | Q(category__parent=obj_id))
            if (len(specif_list) == 1) or (len(set(general_list)) == 1):
                return obj.filter(specificationsvalue__in=specif_list)
            else:
                counter = list(collections.Counter(general_list).values())
                for x in range(len(counter)):
                    if x == 0:
                        querylist = obj.filter(specificationsvalue__in=specif_list[:counter[x]])
                        del specif_list[:counter[x]]
                    else:
                        querylist = querylist.filter(specificationsvalue__in=specif_list[:counter[x]])
                        del specif_list[:counter[x]]
                return querylist
        else:
            return Product.objects.filter(Q(category=obj_id) | Q(category__parent=obj_id))


@permission_classes([AllowAny])
def home(request):
    ctx = {}
    return render(request, 'index.html', ctx)


@permission_classes([AllowAny])
def productdetail(request, id):
    ctx = {}
    obj = Product.objects.get(id=id)
    ctx['product_id'] = obj.id
    return render(request, 'detail.html', ctx)


def catdetail(request, id):
    ctx = {}
    obj = Category.objects.get(id=id, parent__isnull=True)
    ctx['subcat_id'] = obj.id
    return render(request, 'catdetail.html', ctx)


def productlist(request, id):
    ctx = {}
    obj = Category.objects.get(id=id, parent__isnull=False)
    ctx['productlist_detais'] = obj.id
    return render(request, 'listproduct.html', ctx)


@ api_view(['GET'])
@permission_classes([AllowAny])
def discount(request):
    if request.method == 'GET':
        my_obj = Product.objects.filter(discount_status=True)[:5]
        serializer = discountser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def productdetailinfo(request):
    obj_id = request.GET.get('id')
    if obj_id and obj_id.isdigit():
        obj = Product.objects.get(id=obj_id)
        serializer = productser(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
@permission_classes([AllowAny])
def catlist(request):
    if request.method == 'GET':
        my_obj = Category.objects.filter(parent__isnull=True)
        serializer = catser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def childcat(request):
    if request.method == 'GET':
        my_obj = Category.objects.filter(parent__isnull=False)
        serializer = catser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def getcatchild(request):
    if request.method == 'GET':
        obj_id = request.GET.get('id')
        my_obj = Category.objects.filter(parent__isnull=False, parent__id=obj_id)
        serializer = catchildser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def get_catchild_details(request):
    if request.method == 'GET':
        obj_id = request.GET.get('id')
        my_obj = Category.objects.filter(parent__isnull=False, parent__parent=obj_id)
        serializer = catser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def getbrand(request):
    if request.method == 'GET':
        obj_id = request.GET.get('id')
        my_obj = Brand.objects.filter(category__id=obj_id)
        serializer = brandser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def getseller(request):
    if request.method == 'GET':
        obj_id = request.GET.get('id')
        my_obj = Seller.objects.filter(category__id=obj_id)
        serializer = sellerser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET'])
@permission_classes([AllowAny])
def getgeneralspecifications(request):
    if request.method == 'GET':
        obj_id = request.GET.get('id')
        my_obj = GeneralSpecifications.objects.filter(category__id=obj_id)
        serializer = generalspecificationsser(my_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @ api_view(['GET'])
# def catlistid(request):
#     if request.method == 'GET':
#         obj_id = request.GET.get('id')
#         my_obj = Category.objects.filter(Q(parent__parent__isnull=False, id=obj_id))
#         if my_obj:
#             serializer = catser(my_obj, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
