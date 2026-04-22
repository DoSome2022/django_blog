from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>',views.UserDetailView.as_view(), name='user_profile'),
    path('profile/edit/',views.UserProfileUpdateView.as_view(), name='user_profile_edit'),
    path('agents/',views.UserListView.as_view(), name='user_list'),
    path('addagentsfd/',views.add_friend_view,name='add_agents_fd'),

]