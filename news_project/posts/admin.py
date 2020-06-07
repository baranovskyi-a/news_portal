from django.contrib import admin
from .models import Post


def make_pending(modeladmin, request, queryset):
    queryset.update(status='P')


def make_approved(modeladmin, request, queryset):
    queryset.update(status='A')


def make_declined(modeladmin, request, queryset):
    queryset.update(status='D')


class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)
    list_display = ('title', 'author', 'status', 'date')
    list_filter = ('status', 'date')
    ordering = ('-date',)
    actions = [make_pending, make_approved, make_declined]
    list_per_page = 20


make_pending.short_description = "Mark selected posts as pending"
make_approved.short_description = "Mark selected posts as approved"
make_declined.short_description = "Mark selected posts as declined"

admin.site.register(Post, PostAdmin)



