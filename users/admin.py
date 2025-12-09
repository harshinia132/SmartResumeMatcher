from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_candidate', 'is_recruiter', 'is_staff']
    list_filter = ['is_candidate', 'is_recruiter', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_candidate', 'is_recruiter')
        }),
    )

admin.site.register(User, CustomUserAdmin)