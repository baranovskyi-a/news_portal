from django.urls import path
from .views import ConfirmEmail

app_name = 'one_time_codes'
urlpatterns = [
    path('<uuid:otc>/', ConfirmEmail.as_view(), name='confirm_email'),
]