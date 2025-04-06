from django.urls import path
from .views import projects, project, createProject, updateProject, delete_Project




urlpatterns = [
    path('', projects, name='projects'),
    path('project/<str:pk>/', project, name='pp'),
    path('create_projects/', createProject, name='create_projects'),
    path('update_project/<str:pk>/', updateProject, name = 'update_project'),
    path('delete_project/<str:pk>/', delete_Project, name = 'delete_project'),
]