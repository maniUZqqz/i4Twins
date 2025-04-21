from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='chat_list'),  # اینجا نام view باید 'chat_list' باشد
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/create/', views.create_chat, name='create_chat'),

    path('chat/<int:chat_id>/content-json/', views.chat_content_json, name='chat_content_json'),
]















