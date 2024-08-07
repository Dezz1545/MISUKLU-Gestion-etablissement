from django.shortcuts import render, redirect
from accounts.models import UserProfile
from .models import Filière, Niveau, Classe, Etudiant, Matière, Matiere_classe, Professeur, Frais_scolaire, Paiement, Frais_niveau, Note, Event
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm




# Create your views here.
def dashboards_directeur_etudes(request):
    filiere = Filière.objects.all()
    classe = Classe.objects.all()
    etudiant = Etudiant.objects.all()
    request.user.is_authenticated
    # Récupère le profil de l'utilisateur connecté
    user_profile = UserProfile.objects.get(user=request.user)

    # Vérifie si le profil de l'utilisateur est 'Directeur des études' ou 'directeur des études'
    if user_profile.profile.lower() in ['directeur des études', 'directeur des études']:
        # Si le profil correspond, affiche la page HTML appropriée
        profil = 'directeur'
    datas = {
        'profil': profil,
        'filiere': filiere,
        'classe': classe,
        'etudiant': etudiant,
    }
    return render(request, "dashboards-directeur-etudes.html",datas)


def dashboards_comptable(request):  
    somme_montants_total = Frais_scolaire.objects.aggregate(somme=Sum('montant_total')) 
    montant_payes_total = Frais_scolaire.objects.aggregate(somme=Sum('montant_paye')) 
    montant_restants_total = Frais_scolaire.objects.aggregate(somme=Sum('montant_restant')) 
    etudiants = Etudiant.objects.all()
    datas = {
        "total": somme_montants_total['somme'],
        "total_restant": montant_restants_total['somme'],
        "total_paye": montant_payes_total['somme'],
        "etudiants": etudiants
    }
    return render(request, "comptable/index.html",datas)



def dashboards_professeur(request):
                return render(request, "dashboards-professeur.html")

def dashboards_etudiant(request):
    etudiant = Etudiant.objects.get(email = request.user.username)
    datas = {
        'etudiant': etudiant,
    }
    print(etudiant)
    return render(request, "dashboards-etudiant.html",datas)

def calendrier_classe(request,id):
    user = request.user.username
    etudiant = Etudiant.objects.get(email = user)
    classe = Classe.objects.get(id=id)
    events = Event.objects.filter(classe_id = classe)

    datas = {
        "classe": classe,
        'events': events,
        'etudiant': etudiant,

    }

    return render(request, "classe/consulter_calendrier.html", datas)

def creation_filiere(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        # Vérifier si une filière avec le même nom existe déjà
        if Filière.objects.filter(nom_filiere=nom).exists():
            messages.error(request, f'La filière "{nom}" existe déjà.')
            return redirect('creation_filiere')  # Redirection vers la même page
        else:
            # Si la filière n'existe pas déjà, créez-la
            Filière.objects.create(nom_filiere=nom, description=description)
            messages.success(request, f'La filière "{nom}" a été créée avec succès.')
            return redirect('creation_filiere')  # Redirection vers la même page
    return render(request, "creation_filiere.html")

def creation_niveau(request):
    filieres = Filière.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        filiere = request.POST.get('filiere')
        frais = request.POST.get('frais')
        description = request.POST.get('description')
        # recuperer la fililère
        filiere_final = Filière.objects.get(nom_filiere= filiere)
        # Vérifier si une filière avec le même nom existe déjà
        if Niveau.objects.filter(nom_niveau=nom, filiere_associée=filiere_final).exists():
            messages.error(request, f'Le niveau "{nom}" de la filière "{filiere}" existe déjà.')
            return redirect('creation_niveau')  # Redirection vers la même page
        else:
            # Si la filière n'existe pas déjà, créez-la
            Niveau.objects.create(nom_niveau=nom, filiere_associée=filiere_final, frais_scolaire=frais,description=description)
            messages.success(request, f'Le niveau "{nom}" de la filière "{filiere}" a été créé avec succès.')
            return redirect('creation_niveau')  # Redirection vers la même page
    datas = {
        'filieres': filieres
    }
    return render(request, "creation_niveau.html", datas)

def creation_classe(request):
    filieres = Filière.objects.all()
    niveaux = Niveau.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        niveau = request.POST.get('niveau')
        description = request.POST.get('description')
        # recuperer le niveau
        niveau_final = Niveau.objects.get(id= niveau)
        # Vérifier si une filière avec le même nom existe déjà
        if Classe.objects.filter(nom_classe=nom, niveau_associée=niveau_final).exists():
            messages.error(request, f'La classe "{nom}" du niveau "{niveau_final.nom_niveau}" de la filière "{niveau_final.filiere_associée.nom_filiere}" existe déjà.')
            return redirect('creation_classe')  # Redirection vers la même page
        else:
            # Si la filière n'existe pas déjà, créez-la
            Classe.objects.create(nom_classe=nom, niveau_associée=niveau_final, description=description)
            messages.success(request, f'La classe "{nom}" du niveau "{niveau_final.nom_niveau}" de la filière "{niveau_final.filiere_associée.nom_filiere}" a été créée avec succès.')
            return redirect('creation_classe')  # Redirection vers la même page
    datas = {
        'filieres': filieres,
        'niveaux': niveaux
    }
    return render(request, "creation_classe.html", datas)

def creation_matiere(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        # Vérifier si une filière avec le même nom existe déjà
        if Matière.objects.filter(nom_matiere=nom).exists():
            messages.error(request, f'La matière "{nom}" existe déjà.')
            return redirect('creation_matiere')  # Redirection vers la même page
        else:
            # Si la filière n'existe pas déjà, créez-la
            Matière.objects.create(nom_matiere=nom, description=description)
            messages.success(request, f'La matière "{nom}" a été créée avec succès.')
            return redirect('creation_matiere')  # Redirection vers la même page
    return render(request, "creation_matiere.html")

def creation_etudiant(request):
    classes = Classe.objects.all()
    filieres = Filière.objects.all()
    niveaux = Niveau.objects.all()
    if request.method == 'POST':
        # récuperation des données
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        birth = request.POST.get('date')
        place = request.POST.get('place')
        nom_pere = request.POST.get('pere')
        nom_mere = request.POST.get('mere')
        adresse = request.POST.get('adresse')
        sexe = request.POST.get('sexe')
        nationalite = request.POST.get('nationalite')
        affecte = request.POST.get('affecte')
        classe = request.POST.get('classe')
        clas = Classe.objects.get(nom_classe = classe)
        
        if Etudiant.objects.filter(email=email).exists():
            messages.error(request, f'Un Etudiant avec ce "{email}" existe déjà.')
        else:
            # creation de l'étudiant 
            etudiant = Etudiant()
            etudiant.nom = nom
            etudiant.prenom = prenom
            etudiant.email = email
            etudiant.contact = contact
            etudiant.birth_and_place = birth + " " + place
            etudiant.nom_pere = nom_pere
            etudiant.nom_mere = nom_mere
            etudiant.adresse = adresse
            etudiant.sexe = sexe
            etudiant.nationalite = nationalite
            etudiant.classe_associée = clas
            messages.success(request, f'L\'Etudiant "{nom}" a été enregistré avec succès.')
            if affecte != None:
                etudiant.affecte = True
            etudiant.save()

            #Pour une creation automatique du profile avec un mot de passe par défaut (prototype)

            # Diviser le nom de famille en mots et prendre le premier mot
            last_name_first_word = nom.split()[0]
            # Construire le mot de passe en ajoutant "@1234" au premier mot du nom de famille
            password = f"{last_name_first_word.lower()}@1234"  # Ajoutez ici votre logique pour le mot de passe
            
            # creer le user
            user = User.objects.create_user(  # Utiliser create_user pour créer un nouvel utilisateur
                username=email,  # Utiliser l'e-mail comme nom d'utilisateur
                email=email,
                first_name=prenom,
                last_name=nom,
                password=password
            )
            # Créer le UserProfile associé à l'utilisateur
            user_profile = UserProfile.objects.create(
                user=user,
                profile='etudiant'
            )
            # Sauvegarder l'objet UserProfile
            user_profile.save()

            # creation des frais scolaire
            frais_niveau = Frais_niveau(niveau=etudiant.classe_associée.niveau_associée)
            frais = Frais_scolaire()
            frais.etudiant = etudiant
            if affecte != None:
                frais.montant_total = frais_niveau.montant_non_af
            if affecte == True:
                frais.montant_total = frais_niveau.montant_af
            frais.montant_paye = 0
            frais.montant_restant = frais.montant_total
            frais.save()

    datas = {
        'classe': classes,
        'filieres': filieres,
        'niveaux': niveaux
    }
    return render(request, "creation_etudiant.html", datas)

def creation_note(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        etudiant_id = request.POST.get('etudiant_existants')
        matiere_id = request.POST.get('matiere')
        note_value = request.POST.get('note')

        # Créer une instance de Note
        etudiant = Etudiant.objects.get(pk=etudiant_id)
        matiere = Matière.objects.get(pk=matiere_id)
        note = Note.objects.create(etudiant=etudiant, matiere=matiere, note=note_value)

        # Sauvegarder la note dans la base de données
        note.save()

        # Rediriger vers une autre page ou afficher un message de confirmation
        return redirect('creation-note')

    # Si la méthode HTTP est GET, afficher simplement le formulaire
    etudiants = Etudiant.objects.all()
    matieres = Matière.objects.filter(status=True)  # Filtrer les matières actives
    return render(request, "creation_note.html", {"etudiants": etudiants, "matieres": matieres})

def etudiantlist(request):
    etudiants = Etudiant.objects.all()
    datas = {
        'etudiants': etudiants
    }
    return render(request, "liste-etudiants.html", datas)

def listniveau(request):
    niveaux = Niveau.objects.all()
    datas = {
        'niveaux': niveaux
    }
    return render(request, "liste-niveau.html", datas)

def listclasse(request):
    classes = Classe.objects.all().order_by('niveau_associée__filiere_associée', 'niveau_associée__nom_niveau')
    datas = {
        'classes': classes,
    }
    return render(request, "liste-classe.html", datas)

def listefiliere(request):
    filieres = Filière.objects.all()
    datas = {
        'filieres': filieres,
    }
    return render(request, "liste-filiere.html", datas)

def listmatiere(request):
    matieres = Matière.objects.all()
    datas = {
        'matieres': matieres,
    }
    return render(request, "liste_matiere.html", datas)

def cons_calendrier(request,id):
    classe = Classe.objects.get(id=id)
    events = Event.objects.filter(classe_id = classe)

    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    datas = {
        "classe": classe,
        'matiere_classes': matiere_classes,
        'events': events,
    }
    return render(request, "calendar.html",datas)
def listclasse_etud(request,id):
    classe = Classe.objects.get(id=id)
    etudiants = Etudiant.objects.filter(classe_associée=classe, status=True)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    if request.method == 'POST':
        submit_action = request.POST.get('submit_action', '')
        if submit_action == 'retirer_submit':
            etudiant_selectionnees = request.POST.getlist('etudiant[]')
            # Faites quelque chose avec les matières sélectionnées, par exemple :
            Etudiant.objects.filter(id__in=etudiant_selectionnees).update(status=False)
        elif 'modifier_submit' in request.POST:
            etudiant_selectionnees = request.POST.getlist('etudiant[]')
            etudiant = Etudiant.objects.get(id__in=etudiant_selectionnees)
            return redirect('edit_etudiant', id=classe.id, pk=etudiant.id)
        return redirect(request.path)
    datas = {
        "classe": classe,
        'etudiants': etudiants,
        'matiere_classes': matiere_classes,
    }
    return render(request, "classe/liste_classe.html",datas)

def profmatiere(request,id):
    classe = Classe.objects.get(id=id)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    if request.method == 'POST':
        submit_action = request.POST.get('submit_action', '')
        if submit_action == 'retirer_submit':
            matiere_selectionnees = request.POST.getlist('matiere_classe[]')
            # Faites quelque chose avec les matières sélectionnées, par exemple :
            Matiere_classe.objects.filter(id__in=matiere_selectionnees).delete()
        elif 'modifier_submit' in request.POST:
            matiere_selectionnees = request.POST.getlist('matiere_classe[]')
            prof_matiere = Matiere_classe.objects.get(id__in=matiere_selectionnees)
            return redirect('edit_prof_matiere', id=classe.id, pk=prof_matiere.id)
        return redirect(request.path)
    datas = {
        "classe": classe,
        'matiere_classes': matiere_classes,
    }
    return render(request, "classe/prof_matiere.html",datas)

def creation_prof(request):
    matieres = Matière.objects.filter(status = True)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        matieres_ids = request.POST.getlist('matieres[]') # Récupère la liste des ID des matières sélectionnées

        if Professeur.objects.filter(email=email).exists():
            messages.error(request, f'Un professeur avec ce "{email}" existe déjà.')
        else:
            # Par exemple, sauvegarder le professeur avec ses matières enseignées :
            professeur = Professeur.objects.create(nom=nom, prenom=prenom, email=email, contact=telephone)
            professeur.matière_associée.set(matieres_ids) 
            professeur.save()
            messages.success(request, f'Le professeur "{nom}" a été enregistré avec succès.')

            # Diviser le nom de famille en mots et prendre le premier mot
            last_name_first_word = nom.split()[0]
            # Construire le mot de passe en ajoutant "@1234" au premier mot du nom de famille
            password = f"{last_name_first_word.lower()}@1234"  # Ajoutez ici votre logique pour le mot de passe
            
            # creer le user
            user = User.objects.create_user(  # Utiliser create_user pour créer un nouvel utilisateur
                username=email,  # Utiliser l'e-mail comme nom d'utilisateur
                email=email,
                first_name=prenom,
                last_name=nom,
                password=password
            )
            # Créer le UserProfile associé à l'utilisateur
            user_profile = UserProfile.objects.create(
                user=user,
                profile='professeur'
            )
            # Sauvegarder l'objet UserProfile
            user_profile.save()
            # Redirigez l'utilisateur vers la même page après le succès du POST
            return redirect(request.path)
    datas= {
        'matieres': matieres
    }
    return render(request, "creation_prof.html",datas)

def creation_compt(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Ce "{email}" existe déjà.')
        else:
            # Diviser le nom de famille en mots et prendre le premier mot
            last_name_first_word = nom.split()[0]
            # Construire le mot de passe en ajoutant "@1234" au premier mot du nom de famille
            password = f"{last_name_first_word.lower()}@1234"  # Ajoutez ici votre logique pour le mot de passe
            
            # creer le user
            user = User.objects.create_user(  # Utiliser create_user pour créer un nouvel utilisateur
                username=email,  # Utiliser l'e-mail comme nom d'utilisateur
                email=email,
                first_name=prenom,
                last_name=nom,
                password=password
            )
            # Créer le UserProfile associé à l'utilisateur
            user_profile = UserProfile.objects.create(
                user=user,
                profile='comptable'
            )
            # Sauvegarder l'objet UserProfile
            user_profile.save()
            messages.success(request, f'Le Comptable "{nom}" a été enregistré avec succès.')

            # Redirigez l'utilisateur vers la même page après le succès du POST
            return redirect(request.path)
    return render(request, "creation_compt.html")

def ajouter_etudiant(request,id):
    classe = Classe.objects.get(id=id)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    if request.method == 'POST':
        # récuperation des données
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        birth = request.POST.get('date')
        place = request.POST.get('place')
        nom_pere = request.POST.get('pere')
        nom_mere = request.POST.get('mere')
        adresse = request.POST.get('adresse')
        sexe = request.POST.get('sexe')
        nationalite = request.POST.get('nationalite')
        affecte = request.POST.get('affecte')
        
        if Etudiant.objects.filter(email=email).exists():
            messages.error(request, f'Un Etudiant avec ce "{email}" existe déjà.')
        else:
            # creation de l'étudiant 
            etudiant = Etudiant()
            etudiant.nom = nom
            etudiant.prenom = prenom
            etudiant.email = email
            etudiant.contact = contact
            etudiant.birth_and_place = birth + " " + place
            etudiant.nom_pere = nom_pere
            etudiant.nom_mere = nom_mere
            etudiant.adresse = adresse
            etudiant.sexe = sexe
            etudiant.nationalite = nationalite
            etudiant.classe_associée = classe
            messages.success(request, f'L\'Etudiant "{nom}" a été enregistré avec succès.')
            if affecte != None:
                etudiant.affecte = True
            etudiant.save()

            #Pour une crreation automatique du profile avec un mot de passe par défaut (prototype)

            # Diviser le nom de famille en mots et prendre le premier mot
            last_name_first_word = nom.split()[0]
            # Construire le mot de passe en ajoutant "@1234" au premier mot du nom de famille
            password = f"{last_name_first_word.lower()}@1234"  # Ajoutez ici votre logique pour le mot de passe
            
            # creer le user
            user = User.objects.create_user(  # Utiliser create_user pour créer un nouvel utilisateur
                username=email,  # Utiliser l'e-mail comme nom d'utilisateur
                email=email,
                first_name=prenom,
                last_name=nom,
                password=password
            )
            # Créer le UserProfile associé à l'utilisateur
            user_profile = UserProfile.objects.create(
                user=user,
                profile='etudiant'
            )
            # Sauvegarder l'objet UserProfile
            user_profile.save()

            # creation des frais scolaire
            frais_niveau = Frais_niveau(niveau=etudiant.classe_associée.niveau_associée)
            frais = Frais_scolaire()
            frais.etudiant = etudiant
            if affecte != None:
                frais.montant_total = frais_niveau.montant_non_af
            if affecte == True:
                frais.montant_total = frais_niveau.montant_af
            frais.montant_paye = 0
            frais.montant_restant = frais.montant_total
            frais.save()
    datas = {
        "classe": classe,
        'matiere_classes': matiere_classes,
    }    
    return render(request, "classe/ajouter_etudiant.html",datas)

def edit_etudiant(request,id,pk):
    classes = Classe.objects.all()
    filieres = Filière.objects.all()
    niveaux = Niveau.objects.all()
    etudiant = Etudiant.objects.get(id=pk)
    classe = Classe.objects.get(id=id)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)

    elements = etudiant.birth_and_place.split()  # Sépare la chaîne en fonction des espaces
    # Maintenant, elements[0] contient l'année et elements[1] contient la ville
    annee = elements[0]
    ville = elements[1]

    if request.method == 'POST':
        # récuperation des données
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        birth = request.POST.get('date')
        place = request.POST.get('place')
        nom_pere = request.POST.get('pere')
        nom_mere = request.POST.get('mere')
        adresse = request.POST.get('adresse')
        sexe = request.POST.get('sexe')
        nationalite = request.POST.get('nationalite')
        affecte_value = request.POST.get('affecte', False)
        classe_id = request.POST.get('classe')
        clas = Classe.objects.get(id = classe_id)
    
        # Vérifie si un autre étudiant avec le même email existe
        email_avant = etudiant.email
        if Etudiant.objects.exclude(id=pk).filter(email=email_avant).exists():
            messages.error(request, f"Un autre étudiant avec cet email {email_avant} existe déjà.")
        else:
            # modification de l'étudiant 
            etudiant.nom = nom
            etudiant.prenom = prenom
            etudiant.email = email
            etudiant.contact = contact
            etudiant.birth_and_place = birth + " " + place
            etudiant.nom_pere = nom_pere
            etudiant.nom_mere = nom_mere
            etudiant.adresse = adresse
            etudiant.sexe = sexe
            etudiant.nationalite = nationalite
            etudiant.classe_associée = clas
            # Convertir la valeur en booléen correspondant
            affecte = affecte_value == 'on'
            
            # Assigner la valeur à l'attribut affecte de l'objet Etudiant
            etudiant.affecte = affecte
            etudiant.save()
            messages.success(request, f'L\'Etudiant "{nom}" a été modifié avec succès.')

            # creation des frais scolaire
            frais = Frais_scolaire.objects.get(etudiant=etudiant)
            if frais.montant_total == '900000' and affecte == True:
                print('oui')
                frais.montant_total = 1200000
                frais_restant = int(frais.montant_restant)
                frais.montant_restant = frais_restant + 300000
                frais.save()
            elif frais.montant_total == '1200000' and affecte == False:
                print('non')
                frais.montant_total = 900000
                frais_restant = int(frais.montant_restant)
                frais.montant_restant = frais_restant - 300000
                frais.save()
    datas = {
        "classe": classe,
        "etudiant": etudiant,
        'matiere_classes': matiere_classes,
        "annee": annee,
        "ville": ville,
        'classes': classes,
        'filieres': filieres,
        'niveaux': niveaux
    }    
    return render(request, "classe/edit_etudiant.html",datas)

def ajouter_prof_matiere(request,id):
    classe = Classe.objects.get(id=id)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    matieres = Matière.objects.all()
    profs = Professeur.objects.all()
    if request.method == 'POST':
        # récuperation des données
        selected_matiere = request.POST.get('matiere')
        selected_prof = request.POST.get('prof')
        prof_final = Professeur.objects.get(id=selected_prof)
        matiere_final = Matière.objects.get(nom_matiere=selected_matiere)
        if Matiere_classe.objects.filter(classe=classe, matiere=matiere_final).exists():
            messages.error(request, f'La matière est déjà enseigné dans cette classe.')
        else:
            Matiere_classe.objects.create(classe=classe, matiere=matiere_final, professeur=prof_final)
            messages.success(request, f'La matière a été ajoute dans cette classe.')
        # Redirigez l'utilisateur vers la même page après le succès du POST
        return redirect(request.path)
    datas = {
        "classe": classe,
        'matiere_classes': matiere_classes,
        "matieres": matieres,
        "profs": profs,
    }     
    return render(request, "classe/ajouter_prof_matiere.html",datas)

def edit_prof_matiere(request,id,pk):
    classe = Classe.objects.get(id=id)
    matiere_classes = Matiere_classe.objects.filter(classe=classe)
    matiere_modifie = Matiere_classe.objects.get(id=pk)
    profs = Professeur.objects.filter(matière_associée=matiere_modifie.matiere)
    if request.method == 'POST':
        selected_prof = request.POST.get('prof')
        prof_final = Professeur.objects.get(id=selected_prof)
        Matiere_classe.objects.filter(classe=classe, matiere=matiere_modifie.matiere).update(professeur=prof_final)
        messages.success(request, f'Le professeur de cette matière a été modifie.')
        return redirect(request.path)
    datas={
        "classe": classe,
        'matiere_classes': matiere_classes,
        "matiere_modifie": matiere_modifie,
        "profs": profs
    }
    return render(request, "classe/edit_prof_matiere.html",datas)

def ajouter_paiement(request):
    etudiants = Etudiant.objects.all()
    paiements = Paiement.objects.all()
    frais_personnels= Frais_scolaire.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        montant = request.POST.get('montant')
        etudiant = Etudiant.objects.get(email=email)
        frais = Frais_scolaire.objects.get(etudiant=etudiant)
        if int(frais.montant_restant) < int(montant):
            messages.error(request, f'Le montant de {montant} est supérieur au montant restant à payer.')
        else:
            frais.montant_paye = int(frais.montant_paye) + int(montant)
            frais.montant_restant = int(frais.montant_restant) - int(montant)
            frais.save()
            Paiement.objects.create(etudiant=etudiant, montant=montant)
            messages.success(request, f'Le paiement de {montant} par {email} a été enregistre.')
        return redirect(request.path)
    datas= {
        "paiements": paiements,
        "etudiants": etudiants,
        "frais_personnels": frais_personnels,
    }
    return render(request, "comptable/ajouter_paiement.html",datas)

def liste_paiement(request):
    paiements = Paiement.objects.all().order_by('-date_add')
    datas= {
        "paiements": paiements
    }
    return render(request, "comptable/liste_paiements.html",datas)

def liste_etudiant(request):
    frais = Frais_scolaire.objects.all().annotate(
    montant_restant_int=Cast('montant_restant', IntegerField())).order_by('-montant_restant_int')
    datas= {
        "frais": frais,
    }
    return render(request, "comptable/liste_etudiants.html",datas)

def list_notes(request):
    # Récupérer toutes les notes depuis la base de données
    notes = Note.objects.all()
    return render(request, "liste-note.html", {"notes": notes})

def edit_note(request, note_id):
    # Récupérer la note à modifier depuis la base de données
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        # Récupérer les données du formulaire soumis
        note_value = request.POST.get('note')

        # Mettre à jour les champs de la note avec les nouvelles valeurs
        note.note = note_value
        note.save()

        return redirect('liste_note')
    else:
        return render(request, 'edit-note.html', {'note': note})


def frais_etudiant(request,id):
    frai = Frais_scolaire.objects.get(id=id)
    if request.method == 'POST':
        montant = request.POST.get('montant')
        if int(frai.montant_restant) < int(montant):
            messages.error(request, f'Le montant de {montant} est supérieur au montant restant à payer.')
        else:
            frai.montant_paye = int(frai.montant_paye) + int(montant)
            frai.montant_restant = int(frai.montant_restant) - int(montant)
            frai.save()
            Paiement.objects.create(etudiant=frai.etudiant, montant=montant)
            messages.success(request, f'Le paiement de {montant} par {frai.etudiant.email} a été enregistre.')
        return redirect(request.path)
    datas={
        "frai": frai
    }
    return render(request, "comptable/frais_etudiant.html",datas)

def frais_niveau(request):
    niveaux_etudiants = []
    niveaux = Niveau.objects.all()
    
    for niveau in niveaux:
        if not Frais_niveau.objects.filter(niveau=niveau).exists():
            Frais_niveau.objects.create(niveau=niveau)

    frais_niveaus = Frais_niveau.objects.all()

    for frais in frais_niveaus:
        niveau_nom = frais.niveau
        nombre_etudiants = Etudiant.objects.filter(classe_associée__niveau_associée=frais.niveau).count()
        niveaux_etudiants.append({
            'niveau': niveau_nom,
            'nombre_etudiants': nombre_etudiants
        })
    datas= {
        'frais_niveaus': frais_niveaus,
        'niveaux_etudiants': niveaux_etudiants,
    }
    return render(request, "comptable/frais_niveau.html",datas)

def edit_frais_niveau(request,id):
    frais_niveau = Frais_niveau.objects.get(id=id)
    if request.method == 'POST':
        montant_af = request.POST.get('af')
        montant_non_af = request.POST.get('non')
        frais_niveau.montant_af=montant_af
        frais_niveau.montant_non_af=montant_non_af
        frais_niveau.save()

        messages.success(request, f'les Frais du niveau ont été modifies.')
        return redirect('frais_niveau')
    datas = {
        'frais_niveau': frais_niveau
    }
    return render(request, "comptable/edit_frais_niveau.html",datas)

def settings(request):
    return render(request, 'settings.html')


@login_required
def modify_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Rediriger l'utilisateur vers une page de confirmation ou une autre vue
            return redirect('login')  # Remplacez 'dashboards-etudiant' par le nom de la vue de votre tableau de bord
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'modify_password.html', {'form': form})