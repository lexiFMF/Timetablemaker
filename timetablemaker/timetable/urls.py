from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    path('', views.vector_view, name='requirement'),
    path('create_requirement/', views.create_requirement, name='create_requirement'),
    path('edit_timetable/', views.timetable_view, name='edit_timetable'),
]