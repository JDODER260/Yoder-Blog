from re import template
from django.urls import path
from .views import register, profile, DeleteUser
from post.views import PostListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('password_change/done/home/', PostListView.as_view(), 
        name='password_change_done'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('password/reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_complete'),
    path('user/delete/<int:pk>', DeleteUser.as_view(), name="deleteuser"),
    path('password/change/', PasswordChangeView.as_view(template_name='users/password_change.html'), 
        name='password_change'),
]