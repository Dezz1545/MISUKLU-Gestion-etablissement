from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.custom_login, name='login'),  # Utilise notre vue d'authentification personnalisée
    path('logout/', views.custom_logout, name='logout'),  # Utilise notre vue de déconnexion personnalisée
]