from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email','is_staff','is_superuser','is_active','created_date')
    list_filter = ('email','is_staff','is_superuser','is_active','created_date')
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ("Permissions", {'fields': ("is_staff", "is_active", "is_superuser")}),
        ('Groups Permissons', {"fields": ("groups",'user_permissions')}),
        ('Important Dates', {"fields": ("last_login", "created_date")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff"
            )}
         ),
    )
    ordering = ('email',)

admin.site.register(User,CustomUserAdmin)