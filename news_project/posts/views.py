from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import PostForm
from users.models import UserProfile
from django.contrib import messages

# Create your views here.
class AddPostView(View):
    def get(self, request, **kwargs):
        template_name = 'add_post.html'
        args = {'post_form': PostForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
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
            return redirect(reverse('main_page:main_page'))
        return render(request, template_name, context={'post_form': post_form})
