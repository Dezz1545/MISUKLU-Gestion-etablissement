from django.db import models
from django.utils.text import slugify

# Create your models here.
class Filière(models.Model):
    nom_filiere = models.CharField(max_length = 150) 
    description = models.TextField()

    # standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.nom_filiere

class Niveau(models.Model):
    nom_niveau = models.CharField(max_length = 150)
    filiere_associée = models.ForeignKey(Filière, on_delete=models.CASCADE, related_name="niveau")
    description = models.TextField()
    frais_scolaire = models.CharField(max_length = 150)

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.nom_niveau}({self.filiere_associée})"
    
class Matière(models.Model):
    nom_matiere = models.CharField(max_length = 150)
    description = models.TextField()

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.nom_matiere}"


class Professeur(models.Model):
    nom = models.CharField(max_length = 150)
    prenom = models.CharField(max_length = 150)
    email = models.EmailField()
    contact = models.CharField(max_length = 300, blank=True)
    matière_associée = models.ManyToManyField(Matière, related_name='professeur_matière', blank=True)

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Classe(models.Model):
    nom_classe = models.CharField(max_length = 150)
    description = models.TextField()
    niveau_associée = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="classe_niveau")
    matière_associée = models.ManyToManyField(Matière, related_name='classe_matière', blank=True)
    Professeur_associée = models.ManyToManyField(Professeur, related_name='classe_professeur', blank=True)

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.nom_classe}({self.niveau_associée})"
    

class Etudiant(models.Model):
    nom = models.CharField(max_length = 150)
    prenom = models.CharField(max_length = 150)
    email = models.EmailField()
    contact = models.CharField(max_length = 300)
    birth_and_place = models.CharField(max_length = 300)
    nom_pere = models.CharField(max_length = 150)
    nom_mere = models.CharField(max_length = 150)
    adresse = models.CharField(max_length = 250)
    sexe = models.CharField(max_length = 150)
    nationalite = models.CharField(max_length = 200)
    classe_associée = models.ForeignKey(Classe, related_name = 'etudiant_classe', on_delete = models.CASCADE)
    affecte = models.BooleanField(default = False)

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.nom} {self.prenom}"

class Evaluation(models.Model):
    nom = models.CharField(max_length = 150)
    type = models.CharField(max_length = 150)
    classe_associée = models.ForeignKey(Classe, related_name='evaluatuion_classe', on_delete=models.CASCADE)
    matière_associée = models.ForeignKey(Matière, related_name='evaluatuion_matiere', on_delete=models.CASCADE)
    coefficient = models.CharField(max_length = 2)
    date_evaluation = models.DateTimeField(auto_now_add = True)

    #standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.classe_associée} {self.matière_associée} ({self.date_evaluation})"
    
class Note(models.Model):
    evaluation_associee = models.ForeignKey(Evaluation, related_name='evaluatuion_note', on_delete=models.CASCADE, default= None)
    etudiant = models.ForeignKey(Etudiant, related_name='etudiant_note', on_delete=models.CASCADE)
    note = models.CharField(max_length = 150)

    #standards
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.etudiant.nom} {self.evaluation_associee.date_evaluation} ({self.note})"

class Frais_scolaire(models.Model):
    etudiant = models.ForeignKey(Etudiant, related_name='etudiant_solde', on_delete=models.CASCADE)
    montant_total = models.CharField(max_length = 150, default=0)
    montant_paye = models.CharField(max_length = 150, default=0)
    montant_restant = models.CharField(max_length = 150, default=0)

    #standards
    statut = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.etudiant.nom} {self.montant_restant}"

class Matiere_classe(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="classe")
    matiere = models.ForeignKey(Matière, on_delete=models.CASCADE, related_name="classe_matiere")
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE, related_name="classe_prof")

    #standards
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.classe.nom_classe} {self.professeur.nom}({self.matiere.nom_matiere})"
    
class Paiement(models.Model):
    etudiant = models.ForeignKey(Etudiant, related_name='etudiant_paiement', on_delete=models.CASCADE)
    montant = models.PositiveIntegerField(default=0)

    #standards
    statut = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.etudiant} {self.date_add}"
    
class Frais_niveau(models.Model):
    niveau = models.ForeignKey(Niveau, related_name='frais_niveau', on_delete=models.CASCADE)
    montant_af = models.CharField(max_length = 150, default=900000)
    montant_non_af = models.CharField(max_length = 150, default=1200000)

    #standards
    statut = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.niveau.nom_niveau} {self.montant_af}"
    
class Event(models.Model):
    classe_id = models.ForeignKey(Classe, related_name="event", on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.title



    