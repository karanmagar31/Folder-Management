from django import forms
from .models import Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

    # Optional: You can add a custom validation or choice limit for parent folder if needed
