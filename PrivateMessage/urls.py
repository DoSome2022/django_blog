from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.friend_list_view, name='friend_list'),
    path('chat/<int:friend_id>/',views.chat_room,name='chat_room'),
]