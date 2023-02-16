from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    OwnerProfileModel,
    ProviderProfileModel,
    StaffProfileModel,
    TenantProfileModel,
)

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OwnerProfileModel)
admin.site.register(ProviderProfileModel)
admin.site.register(StaffProfileModel)
admin.site.register(TenantProfileModel)