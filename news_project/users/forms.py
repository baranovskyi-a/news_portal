from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile
from django.utils import timezone


def get_years():
    curr_year = timezone.localdate().year
    return range(curr_year - 17, curr_year - 125, -1)


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='email(*)')
    password = forms.CharField(widget=forms.PasswordInput(), label='password(*)')

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years(),  empty_label=('year', 'month', 'day')), required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'surname', 'birth_date']
