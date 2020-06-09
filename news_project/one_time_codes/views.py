from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from .models import OneTimeCode


class ConfirmEmail(View):
    def get(self, request, **kwargs):
        one_time_code = get_object_or_404(
            OneTimeCode,
            code=kwargs.get('otc', -1)
        )
        if one_time_code.is_confirmed:
            messages.add_message(request, messages.INFO, f'Your email is already confirmed')
            return redirect(reverse('posts:list'))
        if one_time_code.is_active:
            one_time_code.is_confirmed = True
            one_time_code.save()
            messages.add_message(request, messages.INFO, f'Your email has been confirmed')
            return redirect(reverse('posts:list'))
        else:
            messages.add_message(request, messages.INFO, f'This token expired')
            return redirect(reverse('posts:list'))
