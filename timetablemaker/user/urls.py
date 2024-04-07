from django.urls import path
from . import views  # Import views from the same app
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='Dashboard'),
    path('account/', views.account_management_view, name='account_management'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]