from django import forms
from .models import UserProfile
from django.contrib.auth.models import User 

class RegistrationForm(forms.ModelForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    profile = forms.ChoiceField(label='Profile', choices=UserProfile.PROFILE_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Profile'}))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'profile']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
