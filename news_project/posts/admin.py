from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)


admin.site.register(Post, PostAdmin)