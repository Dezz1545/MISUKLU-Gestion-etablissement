import datetime
from django.shortcuts import render, redirect
from .models import  Event, Classe
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


def calendar(request):
    events = Event.objects.all()
    datas = {
        'events': events,
    }
    return render(request, "calendar.html", datas)

def all_events(request,id):
    classe = Classe.objects.get(id=id)
    all_events = Event.objects.filter(classe_id = classe)
    out = []
    for event in all_events:
        out.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.strftime("%Y-%m-%dT%H:%M:%S"),  # Format ISO 8601
            'end': event.end.strftime("%Y-%m-%dT%H:%M:%S"),
            'classe_id': event.classe_id.pk,
        })
    return JsonResponse(out, safe=False)

@csrf_exempt  # Utilisé pour autoriser les requêtes POST sans jeton CSRF (pour les démos seulement, à utiliser avec précaution en production)
def add_event(request,id):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', None)
        start = data.get('start', None)
        end = data.get('end', None)
        classe = data.get('classe', None)
        classe = Classe.objects.get(id=id)
        event = Event()
        event.title = title
        event.start = start
        event.end = end
        event.classe_id = classe
        event.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        title = request.GET.get('title', None)
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        event = Event.objects.get(id = id)
        event.title = title
        event.start = start
        event.end = end
        event.save()
        data = {}
    
    return JsonResponse({'success': True})

csrf_exempt
def remove(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_id = data.get('id')
        print(event_id)
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                event.delete()
                return JsonResponse({'success': True})
            except Event.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Event not found'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid event ID'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


# def save_planning(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             semaine = datetime.strptime(data['semaine'], '%Y-%m-%d').date()
#             planning_data = data['planning']
            
#             # Enregistrer le planning dans la base de données
#             planning = Planning.objects.create(semaine=semaine, data=planning_data)
#             planning.save()

#             return JsonResponse({'success': True, 'message': 'Planning sauvegardé avec succès.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'success': False, 'message': 'Requête invalide.'})
