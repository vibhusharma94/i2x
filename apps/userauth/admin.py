from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.userauth import models as userauth_models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models

admin.site.unregister(auth_models.Group)


class CustomTokenInline(admin.StackedInline):
    model = userauth_models.CustomToken


class AccountActivationInline(admin.StackedInline):
    model = userauth_models.AccountActivation


class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'expiry_time', 'created', 'user', 'refresh_token']
    raw_id_fields = ['user']

admin.site.register(userauth_models.CustomToken, CustomTokenAdmin)


class UserAdmin(UserAdmin):
    inlines = [CustomTokenInline, AccountActivationInline]
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_verified']
    list_display_links = ['id', 'email', 'first_name']
    search_fields = ['first_name', 'email']
    readonly_fields = ['date_joined', 'updated_at', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'updated_at',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2',)}
        ),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    ordering = ('-id',)


admin.site.register(userauth_models.User, UserAdmin)


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reset_key']
    search_fields = ['user']
    raw_id_fields = ('user',)

admin.site.register(userauth_models.PasswordReset, PasswordResetAdmin)
