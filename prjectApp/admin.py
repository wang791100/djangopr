# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from prjectApp.models import User,Purchase,PurchaseType
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# admin.site.register(User)

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ('基础设置', {
            'fields': (
                'username','password','count','time'
            )
        }),
    )
    list_display = ('username','count','time')

    add_fieldsets = (
        ('基础设置', {
            'fields': (
                'username', 'password', 'count', 'time'
            )
        }),
    )
admin.site.register(PurchaseType)
admin.site.register(Purchase)
