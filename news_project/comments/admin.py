from django.contrib import admin
from .models import Comment
from django import forms


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'post', )
    list_display = ('first_symbols_of_comment', 'author', 'date', 'post')
    list_filter = ('date', )
    ordering = ('-date',)
    list_per_page = 50

    def first_symbols_of_comment(self, obj):
        return obj.body[:min(len(obj.body), 30)]

    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'body': forms.Textarea}
        return super().get_form(request, obj, **kwargs)


admin.site.register(Comment, CommentAdmin)







