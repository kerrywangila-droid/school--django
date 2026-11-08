from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('theme-generator/', views.theme_generator, name='theme_generator'),
]