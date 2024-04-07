from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    path('hello/', views.hello_world_view, name='hello_world'),  # Map the view to the /hello/ URL path
    path('', views.workday_view, name='Workday'),
    path('create_day/', views.create_day, name='create_day'),
]