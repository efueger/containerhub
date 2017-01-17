# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, SSHKey, Container, Port, Network, IPAddress


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class SSHKeyInline(admin.StackedInline):
    model = SSHKey


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,
               SSHKeyInline]


admin.site.unregister(User)
#admin.site.register(Profile)
admin.site.register(User, UserAdmin)
admin.site.register(Container)
admin.site.register(Port)
admin.site.register(Network)
admin.site.register(IPAddress)

