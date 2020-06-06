from django.urls import path
from .views import AddPostView, PostListView

app_name = 'posts'
urlpatterns = [
    path('add/', AddPostView.as_view(), name='add'),
    path('list/', PostListView.as_view(), name='list'),
]