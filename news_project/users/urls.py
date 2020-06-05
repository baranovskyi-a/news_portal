from django.urls import path
from users.views import UserRegistrationView

app_name = 'users'
urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # path('simple', simple_view),
]