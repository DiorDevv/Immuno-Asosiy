from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name',
        'role_user', 'auth_status', 'is_active', 'is_staff', 'is_superuser',
        'last_login', 'date_joined', 'created_at', 'updated_at'
    )
    list_filter = ('role_user', 'auth_status', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role_user')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Information', {'fields': ('role_user', 'auth_status')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (  # Yangi user qo'shayotganda ushbu maydonlar chiqadi
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role_user', 'auth_status',
            'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
