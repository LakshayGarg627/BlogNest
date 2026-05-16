from django.urls import path
from . import views   # . means current directory
from .views import PostListView,PostDetailView,PostCreateView, PostUpdateView, PostDeleteView,UserPostListView
urlpatterns=[
    path('', PostListView.as_view() ,name='blog-home'),  # Empty path is a home path
    
    path('user/<str:username>', UserPostListView.as_view() ,name='user-posts'),
    
    path('post/<int:pk>/', PostDetailView.as_view() ,name='post-detail'),

    path('post/new/', PostCreateView.as_view() ,name='post-create'),
    
    path('post/<int:pk>/update/', PostUpdateView.as_view() ,name='post-update'),

    path('post/<int:pk>/delete/', PostDeleteView.as_view() ,name='post-delete'),

    path('topic/<str:topic_name>/', views.topic, name='blog-topic'),

    path('about/',views.about,name='blog-about')
]