from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    # For AllAuth
    path('home/', views.home, name='home'),
    path('logoutview/', views.logoutView, name='logoutview'),
    # For AllAuth
    path('profiles/', views.profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfile, name= 'user-profile'),
    path('account/', views.accountUser, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),

    path('add-skill/', views.addSkill, name='add-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('view-message/<str:pk>/', views.viewMessage, name='view-message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
]