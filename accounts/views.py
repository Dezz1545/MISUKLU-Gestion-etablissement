from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import  CustomLoginForm , RegistrationForm
from .models import UserProfile


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)  # Utilisez 'email' comme nom d'utilisateur
            if user is not None:
                login(request, user)
                # Récupérer le profil de l'utilisateur
                try:
                    profile = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                    # Gérer le cas où le profil n'existe pas
                    profile = None

                # Redirection en fonction du profil
                if profile:
                    if profile.profile == 'directeur des études':
                        return redirect('dashboards-directeur-des-etudes')
                    elif profile.profile == 'comptable':
                        return redirect('dashboards-comptable')
                    elif profile.profile == 'professeur':
                        return redirect('dashboards-professeur')
                    elif profile.profile == 'etudiant':
                        return redirect('dashboards-etudiant')
                    else:
                        # Profil non reconnu, rediriger vers une page par défaut
                        return redirect('index')  # Ou une autre page par défaut
                else:
                    # Profil non trouvé, rediriger vers une page par défaut
                    return redirect('index')  # Ou une autre page par défaut

    else:
        form = CustomLoginForm()
    return render(request, "login.html", {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')  # Rediriger l'utilisateur vers la page de connexion après la déconnexion
