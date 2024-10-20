from django.shortcuts import render
from .models import Conferences
from django.views.generic import ListView,DetailView
# Create your views here.
def conferenceList(request):
    liste=Conferences.objects.all().order_by('-start_date')
    print(liste)
    return render(request,'conferences/conferenceListe.html',
                  {'conferenceslist':liste})
class ConferenceListView(ListView):
    model=Conferences
    #template_name=conference/conference/esmfichier html si tu as renommmer le nom du fichier html autre que conferences_list
    context_object_name='conferences'
    def get_queryset(self):
       return Conferences.objects.order_by('-start_date')
class DetailsViewConference(DetailView):
    model=Conferences
    template_name='conferences/conference_detail_view.html'
    context_object_name='conf'
