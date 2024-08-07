from django.urls import path
from . import views, cal_views



urlpatterns = [
    path('dashboards-directeur-etudes/', views.dashboards_directeur_etudes, name='dashboards-directeur-des-etudes'),
    path('dashboards-comptable/', views.dashboards_comptable, name='dashboards-comptable'),
    path('dashboards-professeur/', views.dashboards_professeur, name='dashboards-professeur'),
    path('dashboards-etudiant/', views.dashboards_etudiant, name='dashboards-etudiant'),
    path('creation-filiere/', views.creation_filiere, name='creation_filiere'),
    path('creation-niveau/', views.creation_niveau, name='creation_niveau'),
    path('creation-classe/', views.creation_classe, name='creation_classe'),
    path('creation-etudiant/', views.creation_etudiant, name='creation-etudiant'),
    path('creation-note/', views.creation_note, name='creation-note'),
    path('liste-etudiant/', views.etudiantlist, name='liste_etudiant'),
    path('liste-niveau/', views.listniveau, name='liste_niveau'),
    path('liste-classe/', views.listclasse, name='liste_classe'),
    path('liste-filiere/', views.listefiliere, name='liste_filiere'),
    path('liste-note/', views.list_notes, name='liste_note'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('consulter-calendrier/<int:id>', views.cons_calendrier, name='cons_calendrier'),
    path('liste-de-classe/<int:id>', views.listclasse_etud, name='listclasse_etud'),
    path('creation-matiere/', views.creation_matiere, name='creation_matiere'),
    path('liste-matiere/', views.listmatiere, name='list_matiere'),
    path('prof-classe/<int:id>', views.profmatiere, name='profmatiere'),
    path('creation-prof/', views.creation_prof, name='creation_prof'),
    path('creation-comptable/', views.creation_compt, name='creation_compt'),
    path('ajouter-etudiant/<int:id>', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('edit-etudiant/<int:id>/<int:pk>', views.edit_etudiant, name='edit_etudiant'),
    path('ajouter-prof-matiere/<int:id>', views.ajouter_prof_matiere, name='ajouter_prof_matiere'),
    path('edit-prof-matiere/<int:id>/<int:pk>', views.edit_prof_matiere, name='edit_prof_matiere'),
    path('ajouter-paiement/', views.ajouter_paiement, name='ajouter_paiement'),
    path('liste-paiement/', views.liste_paiement, name='liste_paiement'),
    path('liste-etudiant-comptable/', views.liste_etudiant, name='comp_liste_etudiant'),
    path('frais-etudiant/<int:id>', views.frais_etudiant, name='frais_etudiant'),
    path('liste-frais-niveau/', views.frais_niveau, name='frais_niveau'),
    path('modifie-frais-etudiant/<int:id>', views.edit_frais_niveau, name='edit_frais_niveau'),
    path('calendrier/<int:id>', views.calendrier_classe, name='calendrier'),
    path('consulter-calendrier/all_events/<int:id>', cal_views.all_events, name='all_events'),
    path('add_event/<int:id>', cal_views.add_event, name = 'add_event'), 
    path('remove/', cal_views.remove, name = 'remove'), 
    path('update/', cal_views.update, name = 'update'), 
    path('calendrier/all_events/<int:id>', cal_views.all_events, name='all_events'),
    path('settings/', views.settings, name='settings'),
    path('modify_password/', views.modify_password, name='modify_password'),



]