from django.urls import path
from . import views

urlpatterns = [
    # 🌐 Core Routes
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # 🧑‍💻 Code Collaboration
    path('join/', views.JoinRoomView.as_view(), name='join_room'),
    path('create/', views.CreateRoomView.as_view(), name='create_room'),
    path('room/<str:room_name>/', views.CodeRoomView.as_view(), name='code_room'),

    # 🎯 Profile Interests
    path('update-interests/', views.update_interests, name='update_interests'),

    # 🤖 AI Code Assistant API
    path('ai-autocomplete/', views.HuggingFaceAutocompleteView.as_view(), name='ai_autocomplete'),

]
