from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import User, OtpNumber, UserLocations
import random
from kavenegar import *
from .serializer import CreateUserSerializer, LoginSerializer, UserSerializer, UserLocationsSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import login
from social.serializer import Likeserializer, bookmarkserializer, cummentuserserializer
from social.models import Like, Bookmark, Cumment
import re


reg = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
match_re = re.compile(reg)


def register_page(request):
    return render(request, 'registreation.html')


def passwordrecovery_page(request):
    return render(request, 'passwordrecovery.html')


def login_page(request):
    return render(request, 'login.html')


def set_password(request):
    return render(request, 'set_password.html')


def new_password_replace(request):
    return render(request, 'new_password_replace.html')


@login_required(login_url='/loginuser/')
@permission_classes([IsAuthenticated])
def dashboard_page(request):
    return render(request, 'dashboard.html')


@ api_view(['POST'])
@permission_classes([AllowAny])
def phone_validation(request):
    phonenumber = request.POST.get('phonenumber')
    if phonenumber:
        user = User.objects.filter(phone__iexact=phonenumber)
        if user.exists():
            return Response({
                'status': False,
                'detail': 'این شماره تلفن قبلا در سایت ثبت نام شده است.'
            })
        else:
            key = send_otp(phonenumber)
            if key:
                obj = OtpNumber.objects.filter(phonenumber=phonenumber)
                if obj:
                    objcount = obj.first()
                    if objcount.counts < 7:
                        # api = KavenegarAPI(
                        #     '7952507248584D75533155316553305A71497849324973554D465645566E474851547333537367396E56303D')
                        # params = {
                        #     'receptor': phonenumber,
                        #     'token': key,
                        #     'template': 'Verify',
                        #     'message': 'Kaveh specialized Web service '
                        # }
                        # response = api.verify_lookup(params)
                        objcount.counts += 1
                        objcount.otp_number = key
                        objcount.save()
                        return Response({
                            'status': True,
                            'detail':
                            'کد تایید ارسال شد.'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail':
                            'تعداد درخواست های تایید هویت پیامکی بیش از حد مجاز است لطفا با بخش پشتیبانی تماس فرمایید.'
                        })
                else:
                    # api = KavenegarAPI(
                    #     '7952507248584D75533155316553305A71497849324973554D465645566E474851547333537367396E56303D')
                    # params = {
                    #     'receptor': phonenumber,
                    #     'token': key,
                    #     'template': 'Verify',
                    #     'message': 'Kaveh specialized Web service '
                    # }
                    # response = api.verify_lookup(params)
                    OtpNumber.objects.create(phonenumber=phonenumber, otp_number=key)
                    return Response({
                        'status': True,
                        'detail':
                            'کد تایید ارسال شد.'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'send otp error.'
                })
    else:
        return Response({
            'status': False,
            'detail': 'شماره تلفن وارد نشده است.'
        })


def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False


@ api_view(['POST'])
@permission_classes([AllowAny])
def otp_validator(request):
    otp_number = request.POST.get('otp')
    phonenumber = request.POST.get('phonenumber')
    if otp_number and phonenumber:
        phone = OtpNumber.objects.filter(phonenumber=phonenumber, otp_number=otp_number)
        obj = phone.first()
        if obj and obj.otp_number == otp_number:
            obj.validate = True
            obj.save()
            return Response({
                'status': True,
                'detail': 'کاربر با موفقیت ثبت نام شد.'
            })
        else:
            return Response({
                'status': False,
                'detail': 'کد تایید منطبق نیست.'
            })
    else:
        return Response({
            'status': False,
            'detail': 'کد تایید وارد نشده است.'
        })


@ api_view(['POST'])
@permission_classes([AllowAny])
def registeration(request):
    password = request.POST.get('password')
    phonenumber = request.POST.get('phonenumber')
    if phonenumber and password:
        res = re.search(match_re, password)
        if res:
            myobj = OtpNumber.objects.filter(phonenumber=phonenumber)
            obj = myobj.first()
            if obj:
                if obj.validate:
                    temp_data = {
                        'phone': phonenumber,
                        'password': password,
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    obj.delete()
                    if user:
                        return Response({
                            'status': True,
                            'user': UserSerializer(user).data,
                            'token': AuthToken.objects.create(user)[1],
                            'detail': 'کاربر با موفقیت ثبت نام شد.'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail': 'اوه اوه یه مشکلی پیش اومده.'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'otp تایید نشده است.'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'شماره موبایل پیدا نشد.'
                })
        else:
            return Response({
                'status': False,
                'detail': 'طول پسورد باید حداقل 8 کاراکتر باشد و شامل حداقل یک عدد و یک حرف باشد.'
            })
    else:
        return Response({
            'status': False,
            'detail': 'شماره موبایل یا رمز عبرور وارد نشده است.'
        })


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


@ api_view(['POST'])
@permission_classes([AllowAny])
def phone_validation_passchange(request):
    phonenumber = request.POST.get('phonenumber')
    if phonenumber:
        user = User.objects.filter(phone__iexact=phonenumber)
        if user.exists():
            key = send_otp(phonenumber)
            if key:
                obj = OtpNumber.objects.filter(phonenumber=phonenumber)
                if obj:
                    objcount = obj.first()
                    if objcount.counts < 7:
                        # api = KavenegarAPI(
                        #     '7952507248584D75533155316553305A71497849324973554D465645566E474851547333537367396E56303D')
                        # params = {
                        #     'receptor': phonenumber,
                        #     'token': key,
                        #     'template': 'Verify',
                        #     'message': 'Kaveh specialized Web service '
                        # }
                        # response = api.verify_lookup(params)
                        objcount.counts += 1
                        objcount.otp_number = key
                        objcount.save()
                        return Response({
                            'status': True,
                            'detail':
                            'کد تایید ارسال شد.'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail':
                            'تعداد درخواست های تایید هویت پیامکی بیش از حد مجاز است لطفا با بخش پشتیبانی تماس فرمایید.'
                        })
                else:
                    # api = KavenegarAPI(
                    #     '7952507248584D75533155316553305A71497849324973554D465645566E474851547333537367396E56303D')
                    # params = {
                    #     'receptor': phonenumber,
                    #     'token': key,
                    #     'template': 'Verify',
                    #     'message': 'Kaveh specialized Web service '
                    # }
                    # response = api.verify_lookup(params)
                    OtpNumber.objects.create(phonenumber=phonenumber, otp_number=key)
                    return Response({
                        'status': True,
                        'detail':
                            'کد تایید ارسال شد.'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'send otp error.'
                })
        else:
            return Response({
                'status': False,
                'detail': 'كاربر ژيدا نشد.'
            })

    else:
        return Response({
            'status': False,
            'detail': 'شماره تلفن وارد نشده است.'
        })


@ api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    phonenumber = request.POST.get('phonenumber')
    password = request.POST.get('password')
    if password and phonenumber:
        res = re.search(match_re, password)
        if res:
            myobj = OtpNumber.objects.filter(phonenumber=phonenumber)
            obj = myobj.first()
            if obj:
                if obj.validate:
                    user = User.objects.filter(phone__iexact=phonenumber)
                    if user.exists():
                        myuser = user.first()
                        myuser.set_password(password)
                        myuser.save()
                        obj.delete()
                        return Response({
                            'status': True,
                            'detail': 'پسورد با موفقيت تغيير كرد.'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail': 'كاربر پيدا نشد.'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'otp تایید نشده است.'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'شماره موبایل پیدا نشد.'
                })
        else:
            return Response({
                'status': False,
                'detail': 'طول پسورد باید حداقل 8 کاراکتر باشد و شامل حداقل یک عدد و یک حرف باشد.'
            })
    else:
        return Response({
            'status': False,
            'detail': 'شماره موبایل یا رمز عبرور وارد نشده است.'
        })


@ api_view(['GET'])
@permission_classes([IsAuthenticated])
def userinfo(request):
    user = User.objects.get(phone=request.user.get_username())
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': False,
            'detail': 'کاربر ثبت نام نکرده است.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edituserinfo(request):
    key = request.POST.get('key')
    value = request.POST.get('value')
    user = User.objects.get(phone=request.user.get_username())
    if user and key and value:
        user.__dict__[key] = value
        user.save()
        return Response({
            'status': True,
            'detail': 'ویرایش با موفقیت انجام شد.',
            'value': value,
            'key': key
        })
    else:
        return Response({
            'status': False,
            'detail': 'کاربر پیدا نشد.'
        })


@ api_view(['GET'])
@permission_classes([IsAuthenticated])
def userlocation(request):
    user = User.objects.get(phone=request.user.get_username())
    if user:
        locations = UserLocations.objects.filter(user=user)
        serializer = UserLocationsSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': False,
            'detail': 'کاربر ثبت نام نکرده است.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addnewlocation(request):
    location = request.POST.get('location')
    user = User.objects.get(phone=request.user.get_username())
    if user and location:
        UserLocations.objects.create(user=user, location=location)
        return Response({
            'status': True,
            'detail': 'ادرس با موفقیت افزوده شد.',
        })
    else:
        return Response({
            'status': False,
            'detail': 'کاربر پیدا نشد.'
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuserlike(request):
    if request.user:
        obj = Like.objects.filter(user=request.user)
        serializer = Likeserializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': False,
            'detail': 'کاربر پیدا نشد'
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuserbookmark(request):
    if request.user:
        obj = Bookmark.objects.filter(user=request.user)
        serializer = bookmarkserializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': False,
            'detail': 'کاربر پیدا نشد'
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcummentuser(request):
    if request.user:
        obj = Cumment.objects.filter(user=request.user)
        serializer = cummentuserserializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': False,
            'detail': 'کاربر پیدا نشد'
        })
