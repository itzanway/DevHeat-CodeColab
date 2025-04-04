from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('join/', views.JoinRoomView.as_view(), name='join_room'),
    path('create/', views.CreateRoomView.as_view(), name='create_room'),
    path('room/<str:room_name>/', views.CodeRoomView.as_view(), name='code_room'),
    path('update-interests/', views.update_interests, name='update_interests'),
    path("get_recommended_rooms/", views.get_recommended_rooms, name="get_recommended_rooms"),
]