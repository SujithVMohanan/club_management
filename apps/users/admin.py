from django.contrib import admin
from apps.users.models import Users

# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'is_staff', 'is_active','is_superuser')
