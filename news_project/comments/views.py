from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views.generic import View, ListView
from .forms import CommentForm
from .models import Comment
from posts.models import Post
from users.models import UserProfile
from django.conf import settings
from mailer.sender import send_mail


class AddCommentView(View):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        template_name = 'add_comment.html'
        args = {'comment_form': CommentForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        template_name = 'add_comment.html'
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = get_object_or_404(
                Post,
                pk=kwargs.get('post_id', -1)
            )
            new_comment.author = request.user
            if UserProfile.objects.get(user=new_comment.post.author).email_confirmed:
                comments_link = request.build_absolute_uri(
                    reverse('comments:list',
                            kwargs={'post_id': new_comment.post.pk}))
                html_content = f'You have got a new comment by {new_comment.author.username}:<br>' + \
                               f'{new_comment.body}<br>' + \
                               'Go to comments: <br>' + \
                               f'<a href="{comments_link}">{comments_link}</a>'
                send_mail.delay(from_email=settings.SENDGRID_SENDERS_EMAIL,
                          to_emails=new_comment.post.author.email,
                          subject='New comment notification',
                          html_content=html_content)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = {'post_id': self.kwargs.get('post_id', -1)}
        context.update(args)
        return context