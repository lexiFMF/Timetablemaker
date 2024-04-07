# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = UserProfile
		fields = ('email', 'username', 'password1', 'password2')

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'username')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']  # Add more fields as needed

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Add more fields as needed

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']  # Add more fields as needed


