from django.contrib import admin
from .models import Filière, Niveau, Matière, Professeur, Classe, Etudiant, Evaluation, Note, Frais_scolaire, Matiere_classe, Paiement, Frais_niveau, Event

# Register your models here.

@admin.register(Filière)
class FilièreAdmin(admin.ModelAdmin):
    list_display = ('nom_filiere', 'description', 'status')
    search_fields = ('nom_filiere',)

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom_niveau', 'filiere_associée', 'description', 'frais_scolaire', 'status')
    search_fields = ('nom_niveau', 'filiere_associée',)

@admin.register(Matière)
class MatièreAdmin(admin.ModelAdmin):
    list_display = ('nom_matiere', 'description', 'status',)
    search_fields = ('nom_matiere',)

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'afficher_matieres', 'status',)
    search_fields = ('nom', 'prenom', 'email', 'status',)  # Ne pas inclure 'matière_associée' dans search_fields

    def afficher_matieres(self, obj):
        return ", ".join([matiere.nom_matiere for matiere in obj.matière_associée.all()])
    afficher_matieres.short_description = 'matière_associée'

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom_classe', 'description', 'niveau_associée', 'status',)
    search_fields = ('nom_classe', 'niveau_associée',)

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'contact', 'birth_and_place', 'nom_pere', 'nom_mere', 'adresse', 'sexe', 'nationalite', 'classe_associée', 'affecte', 'status')
    search_fields = ('nom', 'prenom', 'email', 'contact', 'birth_and_place', 'nom_pere', 'nom_mere', 'adresse', 'sexe', 'nationalite', 'classe_associée', 'affecte',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'classe_associée', 'matière_associée', 'coefficient', 'date_evaluation', 'status',)
    search_fields = ('nom', 'type', 'classe_associée', 'matière_associée',)


@admin.register(Frais_scolaire)
class FraisScolaireAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'montant_total', 'montant_paye', 'montant_restant', 'statut',)
    search_fields = ('etudiant', 'statut',)

@admin.register(Matiere_classe)
class Matiere_classeAdmin(admin.ModelAdmin):
    list_display = ('classe', 'professeur', 'matiere',)
    search_fields = ('classe', 'professeur', 'matiere',)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'montant', 'date_add',)
    search_fields = ('etudiant', 'montant', 'date_add',)

@admin.register(Frais_niveau)
class Frais_niveauAdmin(admin.ModelAdmin):
    list_display = ('niveau', 'montant_af', 'montant_non_af',)
    search_fields = ('niveau',)

admin.site.register(Event)

