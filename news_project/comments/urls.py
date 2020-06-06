from django.urls import path
from .views import AddCommentView, CommentListView

app_name = 'comments'
urlpatterns = [
    path('add/', AddCommentView.as_view(), name='add'),
    path('', CommentListView.as_view(), name='list'),
    # path('<pk>/', PostDetailView.as_view(), name='detail'),
]