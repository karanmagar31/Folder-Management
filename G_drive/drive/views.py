from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Folder
from .forms import FolderForm
from django.contrib import messages

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your form. Please check the details and try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Dashboard View
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    folders = Folder.objects.filter(user=request.user, parent_folder=None)
    return render(request, 'dashboard.html', {'folders': folders})

# Folder View
def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = Folder.objects.filter(parent_folder=folder)
    return render(request, 'folder_view.html', {'folder': folder, 'subfolders': subfolders})

# Folder Creation View
def create_folder(request, parent_folder_id=None):
    parent_folder = get_object_or_404(Folder, id=parent_folder_id) if parent_folder_id else None
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.user = request.user
            new_folder.parent_folder = parent_folder
            new_folder.save()
            if parent_folder:
                return render(request, 'folder_view.html', {'folder': parent_folder, 'subfolders': Folder.objects.filter(parent_folder=parent_folder)})
            return render(request, 'dashboard.html', {'folders': Folder.objects.filter(user=request.user, parent_folder=None)})
    else:
        form = FolderForm()
    return render(request, 'create_folder.html', {'form': form, 'parent_folder': parent_folder})

# Folder Update View
def update_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder_view', folder_id=folder.id)
    else:
        form = FolderForm(instance=folder)
    return render(request, 'update_folder.html', {'form': form, 'folder': folder})

# Folder Deletion View
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if folder.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this folder.")
    parent_folder = folder.parent_folder
    folder.delete()
    if parent_folder:
        return redirect('folder_view', folder_id=parent_folder.id)
    return redirect('dashboard')
