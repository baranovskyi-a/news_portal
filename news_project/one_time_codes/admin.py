from django.contrib import admin
from .models import OneTimeCode
from django import forms


class OneTimeCodeAdmin(admin.ModelAdmin):
    list_per_page = 50
    readonly_fields = ('is_active',)


admin.site.register(OneTimeCode, OneTimeCodeAdmin)
