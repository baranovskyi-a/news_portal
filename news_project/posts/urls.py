from django.urls import path
from .views import AddPostView

app_name = 'posts'
urlpatterns = [
    path('add/', AddPostView.as_view(), name='add'),
]