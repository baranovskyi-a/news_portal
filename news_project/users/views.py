from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, LoginForm
from django.contrib import messages
from one_time_codes.models import OneTimeCode
from django.conf import settings
from mailer.sender import send_mail

class UserRegistrationView(View):

    def get(self, request, **kwargs):
        template_name = 'registration.html'
        args = {'user_form': UserForm(), 'user_profile_form': UserProfileForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        template_name = 'registration.html'
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            cd_user = user_form.cleaned_data
            if User.objects.filter(username=cd_user['email']):
                messages.add_message(request, messages.ERROR, 'This email already exists')
                args = {'user_form': user_form, 'user_profile_form': user_profile_form}
                return render(request, template_name, context=args)
            new_user = user_form.save(commit=False)
            new_user.set_password(cd_user['password'])
            new_user.username = new_user.email
            new_user.save()
            new_profile = user_profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            one_time_code = OneTimeCode.objects.create(user=new_user)
            verification_link = request.build_absolute_uri(
                reverse('one_time_codes:confirm_email',
                        kwargs={'otc': one_time_code.code}))
            html_content = 'Please <b>click</b> for verify your email:<br>' + \
                           f'<a href="{verification_link}">{verification_link}</a>'
            send_mail.delay(from_email=settings.SENDGRID_SENDERS_EMAIL,
                      to_emails=new_user.email,
                      subject='Email verification',
                      html_content=html_content)
            messages.add_message(request, messages.INFO, 'Check your email and confirm the registration')
            return redirect(reverse('posts:list'))
        return render(request, template_name, context={'user_form': user_form, 'user_profile_form': user_profile_form})


class UserLoginView(View):

    def get(self, request, **kwargs):
        template_name = 'login.html'
        args = {'login_form': LoginForm()}
        return render(request, template_name, context=args)

    def post(self, request, **kwargs):
        template_name = 'login.html'
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password']
            )
            if user is None:
                messages.add_message(request, messages.ERROR, 'Wrong email/password')
                args = {'login_form': form}
                return render(request, template_name, context=args)

            login(request, user)
            # messages.add_message(request, messages.INFO, f'Hello, {user.username}')
            return redirect(reverse('posts:list'))
        return render(request, template_name, {'form': form})


class UserLogoutView(View):

    def get(self, request, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, 'Successfully logged out')
        return redirect(reverse('posts:list'))
