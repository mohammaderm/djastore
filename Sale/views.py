from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, ProductCart
from rest_framework import status
from .serializer import ProductCartserializer


def cart_page(request):
    return render(request, 'cart.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_productcart(request):
    if request.user:
        productid = request.POST.get('id')
        quantity = request.POST.get('quantity')
        if productid and quantity:
            if ProductCart.objects.filter(user=request.user, product_id=productid):
                obj = ProductCart.objects.filter(user=request.user, product_id=productid)
                myobj = obj.first()
                myobj.quantity += 1
                myobj.save()
                return Response({
                    'status': True,
                    'detail':
                    'اضافه شد'
                })
            else:
                ProductCart.objects.create(user=request.user, quantity=quantity, product_id=productid)
                return Response({
                    'status': True,
                    'detail':
                    'به سبد خرید اضافه شد.'
                })
        else:
            return Response({
                'status': False,
                'detail':
                'ایتدا یک محصول را وارد کنید'
            })
    else:
        return Response({
            'status': False,
            'detail':
            'ابتدا در سایت ثبت نام کنید.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_productcart(request):
    product_cart_id = request.POST.get('id')
    quantity = request.POST.get('quantity')
    if quantity == 'increase':
        obj = ProductCart.objects.filter(id=product_cart_id)
        myobj = obj.first()
        myobj.quantity += 1
        myobj.save()
        return Response({
            'status': True,
            'detail':
            'اضافه شد'
        })
    elif quantity == 'decrease':
        obj = ProductCart.objects.filter(id=product_cart_id)
        myobj = obj.first()
        myobj.quantity -= 1
        myobj.save()
        return Response({
            'status': True,
            'detail':
            'کم شد'
        })

    else:
        return Response({
            'status': False,
            'detail':
            'تعریف نشده.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_productcart(request):
    product_cart_id = request.POST.get('id')
    if product_cart_id:
        ProductCart.objects.filter(id=product_cart_id).delete()
        return Response({
            'status': True,
            'detail':
            'حذف شد'
        })
    else:
        return Response({
            'status': True,
            'detail':
            'ابتدا محصول را انتخاب کنید'
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_productcart(request):
    if request.user:
        obj = ProductCart.objects.filter(user=request.user)
        serializer = ProductCartserializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': True,
            'detail':
            'ابتدا در سایت ثبت نام کنید.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_order(request):
    if request.user:
        if ProductCart.objects.filter(user=request.user):
            if Cart.objects.filter(user=request.user):
                cartobj = Cart.objects.filter(user=request.user)
                obj = ProductCart.objects.filter(user=request.user)
                for obj1 in obj:
                    obj1.cart = cartobj.first()
                    obj1.save()
                return Response({
                    'status': True,
                    'detail':
                    'سفارش ابدیت شد.'
                })
            else:
                cart_obj = Cart.objects.create(user=request.user)
                obj = ProductCart.objects.filter(user=request.user)
                for obj1 in obj:
                    obj1.cart = cart_obj
                    obj1.save()
                return Response({
                    'status': True,
                    'detail':
                    'سفارش درست شد.'
                })
        else:
            return Response({
                'status': False,
                'detail':
                'هیچ محصولی ثبت نشده است.'
            })

    else:
        return Response({
            'status': False,
            'detail':
            'ابتدا در سایت ثبت نام کنید.'
        })
