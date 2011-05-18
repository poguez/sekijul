####################
#      		   #
#    event.views   #
#       	   #
####################
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from events.models import Event#, EventForm
from django.shortcuts import render_to_response, get_object_or_404
import datetime
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_protect
from forms import *

def index(request):
  latest_event_list = Event.objects.all().order_by('-pub_date')[:5] 
  t = loader.get_template('events/index.html')
  c = Context({
  	'latest_event_list': latest_event_list,
  })
  return HttpResponse(t.render(c))

@csrf_protect
def detail(request, event_id):
#  c={}
  e = get_object_or_404(Event, pk=event_id)

#  c.update(csrf(request))  
  return render_to_response('events/detail.html',{'event':e}, context_instance=RequestContext(request))

#def newPost(request):
  #We create a default event
#  e =  Event(name = "default",date = datetime.datetime.now(),place = "none", category = "none", rating =0, pub_date = datetime.datetime.now(), image ="" )
#  e.save()

#First we create a form instance from the last event created
#  e = Event.objects.get(pk=len(Event.objects.all()))
#  f = EventForm(request.POST, instance = e )
#  f.save()  
#  return HttpResponse(formset)

def newPost(request):
  #We create a default event
  e =  Event(name = "default",date = datetime.datetime.now(),place = "",  rating =0, pub_date = datetime.datetime.now(), image ="" )
  e.save()
  
  EventFormSet = modelformset_factory(Event, exclude=('pub_date','rating'),max_num=1)
  formset = EventFormSet(queryset=Event.objects.order_by('-date'))[:1]
  #formset = EventFormSet(request.POST)

  return HttpResponse(formset)


#def modPost(request):
#  e.name=
#  e.date=
#  e.place=
#  e.category=
#  e.rating=
#  e.pub_date=
#  e.image=

#  e.save()
