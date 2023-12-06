from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
