from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email', 'username', 'first_name',
        'last_name', 'is_staff', 'is_active',
        'profile_picture'
    )
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info',
            {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'username', 'password1', 'password2',
                    'is_staff', 'is_active', 'profile_picture'
                )
            }
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
