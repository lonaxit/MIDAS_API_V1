from django.contrib import admin
# import these because of custom user


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    
    model = CustomUser
    list_display = ['first_name','last_name','username','ippis_number','dob','dofa','is_staff','is_account','is_employee','is_normal']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name','ippis_number','dob','dofa')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_account', 'is_normal', 'is_employee')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name','ippis_number','dob','dofa')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_account', 'is_normal', 'is_employee')
        })
    )
    


 
admin.site.register(CustomUser,CustomUserAdmin)


