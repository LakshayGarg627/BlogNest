from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")
    email=forms.EmailField()

    class Meta:
        model=User
        
        fields=['full_name', 'username', 'email']

    def save(self, commit=True):
        
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()
        
       
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
                
      
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(disabled=True)

    class Meta:
        model=User
        fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
        widgets = {
            'image': forms.FileInput()
        }