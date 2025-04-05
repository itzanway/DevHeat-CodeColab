from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('join/', JoinRoomView.as_view(), name='join_room'),
    path('create/', CreateRoomView.as_view(), name='create_room'),
    path('room/<str:room_name>/', CodeRoomView.as_view(), name='code_room'),
    path('update-interests/', update_interests, name='update_interests'),
]