from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PROFILE_CHOICES = [
        ('directeur des études', 'Directeur des études'),
        ('comptable', ' Comptable'),
        ('professeur', 'Professeur'),
        ('etudiant', 'Etudiant'),
    ]
    profile = models.CharField(max_length=255, choices=PROFILE_CHOICES)

    # Ajout des variables pour savoir si l'utilisateur est connecté et la date de dernière connexion
    is_online = models.BooleanField(default=False)
    last_login_date = models.DateTimeField(default=timezone.now)

    # #Standards
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

