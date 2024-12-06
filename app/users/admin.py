from django.contrib import admin
from .models import Profile, User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
