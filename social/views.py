from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Like, Bookmark, Cumment
from .serializer import CummentSerialzer
from rest_framework import status


@api_view(['POST'])
@login_required
@permission_classes([IsAuthenticated])
def like(request):
    if request.user.is_authenticated:
        obj_id = request.POST.get('id')
        if obj_id:
            if Like.objects.filter(user=request.user, product_id=obj_id):
                Like.objects.filter(user=request.user, product_id=obj_id).delete()
                return Response({
                    'status': True,
                    'detail': 'لایک برداشته شد.'
                })
            else:
                Like.objects.create(user=request.user, product_id=obj_id)
                return Response({
                    'status': True,
                    'detail': 'لایک شد'
                })
        return Response({
            'status': False,
            'detail': 'یه مشکلی پیش اومده.'
        })
    else:
        return Response({
            'status': False,
            'detail': 'برای لایک کردن ابتدا باید در سایت ثبت نام کنید.'
        })


@api_view(['POST'])
@login_required
@permission_classes([IsAuthenticated])
def bookmark(request):
    if request.user.is_authenticated:
        obj_id = request.POST.get('id')
        if obj_id:
            if Bookmark.objects.filter(user=request.user, product_id=obj_id):
                Bookmark.objects.filter(user=request.user, product_id=obj_id).delete()
                return Response({
                    'status': True,
                    'detail': 'لایک برداشته شد.'
                })
            else:
                Bookmark.objects.create(user=request.user, product_id=obj_id)
                return Response({
                    'status': True,
                    'detail': 'لایک شد'
                })
        return Response({
            'status': False,
            'detail': 'یه مشکلی پیش اومده.'
        })
    else:
        return Response({
            'status': False,
            'detail': 'برای نشان کردن ابتدا باید در سایت ثبت نام کنید.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likedisplay(request):
    obj_id = request.POST.get('id')
    if obj_id and Like.objects.filter(user=request.user, product_id=obj_id):
        return Response({'status': True, })
    else:
        return Response({'status': False, })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmarkdisplay(request):
    obj_id = request.POST.get('id')
    if obj_id and Bookmark.objects.filter(user=request.user, product_id=obj_id):
        return Response({'status': True, })
    else:
        return Response({'status': False, })


@api_view(['POST'])
@login_required
@permission_classes([IsAuthenticated])
def cumment(request):
    if request.user.is_authenticated:
        obj_id = request.POST.get('id')
        if obj_id:
            cumment = request.POST.get('cumment')
            title = request.POST.get('title')
            if title and cumment:
                Cumment.objects.create(user=request.user, product_id=obj_id, title=title, value=cumment)
                return Response({
                    'status': True,
                    'detail': 'کامنت پس از تایید در سایت نمایش داده میشود.'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'کامنت یا سر تیتر کامنت خالی است.'
                })
        else:
            return Response({
                'status': False,
                'detail': 'یه مشکلی پیش اومده.'
            })
    else:
        return Response({
            'status': False,
            'detail': 'برای نظر دادن ابتدا باید در سایت ثبت نام کنید.'
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def cummentdisplay(request):
    obj_id = request.GET.get('id')
    if obj_id:
        obj = Cumment.objects.filter(product_id=obj_id, validation=True)
        if obj:
            serializer = CummentSerialzer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'status': False})
    else:
        return Response({
            'status': False,
            'detail': 'یه مشکلی وجود داره.'
        })
