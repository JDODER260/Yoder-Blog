from django.urls import path
from .views import UserPostListView, PostCreateView, PostUpdateView, PostDeleteView, LikeView, CreateComment, DeleteComment ,viewpost, PostListView, UserLikeView




urlpatterns = [
    path('user/<str:username>/', UserPostListView.as_view(),name='user-posts'),
    path('user/like/<int:pk>', UserLikeView, name='like_user'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('post/comment/<int:pk>', CreateComment.as_view(), name='createcomment'),
    path('post/comment/delete/<int:pk>', DeleteComment.as_view(), name='deletecomment'),
    path('post/<int:pk>/', viewpost, name='post-detail'),
]