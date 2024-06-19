from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import AddGroupForm
from .models import User, Group

class GroupAdmin(admin.ModelAdmin):
    form = AddGroupForm
    #fields = ['name', 'permissions', 'is_responsible']

    filter_horizontal = ['permissions']

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)