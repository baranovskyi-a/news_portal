from django.contrib import admin
from .models import UserProfile


def make_admin(modeladmin, request, queryset):
    queryset.update(group='A')


def make_editor(modeladmin, request, queryset):
    queryset.update(group='E')


def make_user(modeladmin, request, queryset):
    queryset.update(group='U')


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'group',)
    list_filter = ('group',)
    readonly_fields = ('email_confirmed',)
    actions = [make_admin, make_editor, make_user]
    list_per_page = 20


make_admin.short_description = "Add selected profile to admin group"
make_editor.short_description = "Add selected profile to editor group"
make_user.short_description = "Add selected profile to user group"

admin.site.register(UserProfile, UserProfileAdmin)