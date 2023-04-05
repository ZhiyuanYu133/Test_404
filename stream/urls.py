from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='stream-home'),
    path('post/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<uuid:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<uuid:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<uuid:pk>/comment/', CommentCreateView.as_view(), name='post-comments'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='stream-about'),
    path('welcome/', views.welcome, name = 'welcome')
]
