from django.urls import path
from .views import ChatView, CreateChat, close


urlpatterns = [
    path('chat/<int:pk>/', ChatView, name='chat'),
    path('chat/new/<int:pk>/', CreateChat.as_view(), name='create_chat'),
    path('close', close, name='close'),
]