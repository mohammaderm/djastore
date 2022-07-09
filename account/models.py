from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):

        if not phone:
            raise ValueError('Users must have an phone number.')
        if not password:
            raise ValueError('Users must have an password.')

        user = self.model(phone=phone, **extra_fields)

        user.set_password(password)
        # user_obj.staff = is_staff
        # user_obj.admin = is_admin
        # user_obj.active = is_active
        user.save()
        return user

    # def create_staffuser(self, phone, password=None):
    #     user = self.create_user(phone, password=password, is_staff=True)
    #     return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_regex = RegexValidator(
        regex=r'(\+98|0)?9\d{9}',
        message="phone number mustbe entered in the format:'+99999999'. up tho 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    job = models.CharField(max_length=20, null=True, blank=True)
    national_code = models.PositiveIntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # first_login = models.BooleanField(default=False)
    # date_of_birth = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.is_staff

    # @property
    # def is_admin(self):
    #     return self.is_admin

    # @property
    # def is_active(self):
    #     return self.is_active


class UserLocations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.phone


class OtpNumber(models.Model):
    phonenumber = models.CharField(max_length=25, null=True)
    otp_number = models.CharField(max_length=25, null=True)
    counts = models.PositiveIntegerField(default=0, null=True, blank=True)
    validate = models.BooleanField(default=False)

    def __str__(self):
        return self.phonenumber
