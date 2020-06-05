from django.urls import path
from .views import main_page
from django.views.generic import TemplateView

app_name = 'main_page'
urlpatterns = [
    path('', main_page, name='main_page'),
]