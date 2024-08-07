from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    profile = forms.ChoiceField(label='Profile', choices=UserProfile.PROFILE_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Profile'}))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'profile', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Veuillez entrer un identifiant et un mot de passe valides.",
        'inactive': "Ce compte est inactif.",
    }
