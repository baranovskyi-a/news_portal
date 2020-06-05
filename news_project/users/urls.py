from django.urls import path
from users.views import UserRegistrationView, UserLoginView, UserLogoutView

app_name = 'users'
urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]