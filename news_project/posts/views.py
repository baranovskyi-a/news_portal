from django.shortcuts import render, redirect, reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import View, ListView, DetailView
from .forms import PostForm
from users.models import UserProfile
from django.contrib import messages
from .models import Post


class AddPostView(View):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        template_name = 'add_post.html'
        args = {'post_form': PostForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        template_name = 'add_post.html'
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            if UserProfile.objects.get(user=request.user).group in ['A', 'E']:
                new_post.status = 'A'
                status_label = 'published'
            else:
                new_post.status = 'P'
                status_label = 'is pending'
            new_post.save()
            messages.add_message(request, messages.INFO, f'Your post {status_label}')
            return redirect(reverse('posts:list'))
        return render(request, template_name, context={'post_form': post_form})


class PostListView(ListView):

    model = Post
    paginate_by = 10
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(status='A')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
