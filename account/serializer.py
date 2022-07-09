from rest_framework import serializers
from .models import UserLocations
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_fields = {'password': {'write_only': True}, }


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'), phone=phone, password=password)
            else:
                msg = {
                    'detail': 'شماره تلفن ژيدا نشد.',
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail': 'شماره تلفن يا پسورد اشتباه است.',
                    'status': False
                }
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {
                'detail': 'شماره تلفن و پسورد وارد نشده است.',
                'status': False
            }
            raise serializers.ValidationError(msg, code='authorization')
        data['user'] = user
        return data


class UserLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocations
        fields = '__all__'
