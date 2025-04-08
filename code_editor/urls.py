from django.urls import path
from . import views
from .views import health_check

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('join/', views.JoinRoomView.as_view(), name='join_room'),
    path('create/', views.CreateRoomView.as_view(), name='create_room'),
    path('room/<str:room_name>/', views.CodeRoomView.as_view(), name='code_room'),
    path('update-interests/', views.update_interests, name='update_interests'),
    path('ai-autocomplete/', views.HuggingFaceAutocompleteView.as_view(), name='ai_autocomplete'),
    path('migrate-now/', migrate_now),
    path('', health_check),
]
