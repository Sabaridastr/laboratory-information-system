from django.contrib import admin
from .models import User, Patient


# ✅ Custom User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')


# ✅ Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'disease', 'created_at')
    list_filter = ('disease', 'created_at')
    search_fields = ('name', 'disease')
    ordering = ('-created_at',)