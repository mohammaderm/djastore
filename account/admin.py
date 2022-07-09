from django.contrib import admin
from .models import OtpNumber, UserLocations

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm

from django.contrib.auth import get_user_model
User = get_user_model()

# admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'is_superuser',
        'last_login',
    )
    search_fields = ('phone',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')


admin.site.register(User, UserAdmin)


class OtpNumberAdmin(admin.ModelAdmin):
    list_display = (
        'phonenumber',
        'otp_number',
        'counts',
        'validate',
    )
    search_fields = ('phonenumber',)
    list_filter = ('counts', 'validate',)


admin.site.register(OtpNumber, OtpNumberAdmin)


class UserLocationsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'location',
    )
    search_fields = ('user',)
    list_filter = ('user', 'location',)


admin.site.register(UserLocations, UserLocationsAdmin)
# class UserAdmin(BaseUserAdmin):
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#     list_display = ('name', 'phone', 'admin')
#     list_filter = ('staff', 'active', 'admin')
#     fieldsets = (
#         (None, {'fields': ('phone', 'password')}),
#         ('Personal info', {'fields': ('name',)}),
#         ('Permissions', {'fields': ('admin', 'staff', 'active')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone', 'password1', 'password2')
#         })
#     ),

#     search_fields = ('phone', 'name')
#     ordering = ('phone', 'name')
#     filter_horizonal = ()

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(UserAdmin, self).get_inline_instances(request, obj)
