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

"""
###########################
#For Registering the Event#
###########################

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      event = Event(
        name = form.cleaned_data['name'],
        date = form.cleaned_data['date'],
        place = form.cleaned_data['place'],
        source = form.cleaned_data['source'],
        content = form.cleaned_data['content'],
        rating = Decimal(0),
        pub_date = datetime.datetime.now(),
        Image = form.cleaned_data['image']
      )
    return HttpResponseRedirect('/register/success')
  else:
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
  return render_to_response(
    'registration/register.html',
    variables
  )

"""
