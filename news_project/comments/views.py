from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views.generic import View, ListView
from .forms import CommentForm
from .models import Comment
from posts.models import Post


class AddCommentView(View):
    def get(self, request, **kwargs):
        template_name = 'add_comment.html'
        args = {'comment_form': CommentForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        template_name = 'add_comment.html'
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = get_object_or_404(
                Post,
                pk=kwargs.get('post_id', -1)
            )
            new_comment.author = request.user
            new_comment.save()
            messages.add_message(request, messages.INFO, 'Your comment added')
            return redirect(reverse('posts:detail', args=[kwargs.get('post_id'),]))
        return render(request, template_name, context={'comment_form': comment_form})


class CommentListView(ListView):

    model = Comment
    paginate_by = 10
    template_name = 'comment_list.html'

    def get_queryset(self):
        post = get_object_or_404(
                Post,
                pk=self.kwargs.get('post_id', -1)
            )
        return Comment.objects.filter(post=post)