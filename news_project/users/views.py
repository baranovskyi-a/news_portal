from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm
from django.contrib import messages


class UserRegistrationView(TemplateView):

    def get(self, request, **kwargs):
        template_name = 'registration.html'
        args = {'user_form': UserForm(), 'user_profile_form': UserProfileForm()}
        return render(request, template_name, context=args)

    def post(self, request):
        template_name = 'registration.html'
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
        if User.objects.filter(username=request.POST['email']):
            messages.add_message(request, messages.ERROR, 'This email already exists')
            args = {'user_form': user_form, 'user_profile_form': user_profile_form}
            return render(request, template_name, context=args)
        if user_form.is_valid() and user_profile_form.is_valid():
            template_name = 'message_page.html'
            new_user = user_form.save(commit=False)
            new_user.username = new_user.email
            new_user.save()
            new_profile = user_profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            messages.add_message(request, messages.INFO, 'Check your email and confirm the registration')
            return redirect(reverse('main_page:main_page'))
        return render(request, template_name, context={user_form: user_form, user_profile_form: user_profile_form})
