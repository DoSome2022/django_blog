from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.MessageCreateView.as_view(), name='realtime_chat'),

]