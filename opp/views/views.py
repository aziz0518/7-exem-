from django.urls import reverse_lazy
from django.views.generic import View,  CreateView
from django.shortcuts import redirect, render
from opp.forms import MemberForm, PersonForm, EventForm
from opp.models import Events, Person
# Create your views here.


def index(request):
    events = Events.objects.all()
    persons = Person.objects.all()
    context = {
        'events': events,
        'persons': persons
    }
    return render(request, 'opp/index.html', context)




def detail_event(request):
    event = Events.objects.all()
    context = {
        'event': event
    }
    return render(request, 'opp/event-detail.html', context)

def listing(request):
    return render(request, 'opp/event-listing.html')



class MemberAdd(View):
    def get(self, request):
        form = MemberForm()
        return render(request, 'opp/member.html', {'form': form})

    def post(self, request):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'opp/member.html', {'form': form})



class PersonAddView(CreateView):
    model = Person
    template_name = 'opp/add-person.html'
    form_class = PersonForm
    success_url = reverse_lazy('index')



def add_events(request):
    event = Events.objects.all()
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EventForm()

    context = {
        'add_event': event,
        'form': form
    }
    return render(request, 'opp/add-event.html', context)
