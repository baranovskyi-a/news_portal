from django.urls import path, include
from .views import AddPostView, PostListView, PostDetailView

app_name = 'posts'
urlpatterns = [
    path('add/', AddPostView.as_view(), name='add'),
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
]