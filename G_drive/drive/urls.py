from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # User registration and login
    path('register/', views.register, name='register'),  # URL for user registration
    path('login/', views.user_login, name='login'),  # URL for user login

    # Dashboard and folder navigation
    path('dashboard/', views.dashboard, name='dashboard'),  # URL for the user's dashboard (home page)
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),  # URL to view a specific folder and its subfolders

    # Folder management (create and delete)
    path('folder/create/', views.create_folder, name='create_folder'),  # For root folders
    path('folder/<int:parent_folder_id>/create/', views.create_folder, name='create_subfolder'),  # For subfolders
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # This handles the logout view

    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),  # Folder view
    path('folder/<int:folder_id>/update/', views.update_folder, name='update_folder'),
    path('folder/<int:folder_id>/delete/', views.delete_folder, name='delete_folder')
]
