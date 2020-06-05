from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from .models import UserProfile
# Create your views here.

from django.views.generic import TemplateView


class UserRegistrationView(TemplateView):

    def get(self, request, **kwargs):
        template_name = 'registration.html'
        args = {'user_form': UserForm(), 'user_profile_form': UserProfileForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        template_name = 'message_page.html'
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = new_user.email
            new_user.save()
            new_profile = user_profile_form.save(commit=False)
            new_profile.user=new_user
            new_profile.save()
        return render(request, template_name, context={user_form: user_form, user_profile_form: user_profile_form})

