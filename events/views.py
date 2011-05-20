####################
#      		   #
#    event.views   #
#       	   #
####################
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from events.models import Event
from django.shortcuts import render_to_response, get_object_or_404
import datetime
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_protect
from forms import *

def index(request):
  latest_event_list = Event.objects.all().order_by('-pub_date')[:20]
  return render_to_response('events/index.html', {"latest_event_list":latest_event_list}, context_instance=RequestContext(request))

@csrf_protect
def detail(request, event_id):
  e = get_object_or_404(Event, pk=event_id)
  if(e):
    date = e.date.date()
    time = e.date.time()
  return render_to_response('events/detail.html',{'event':e, 'date':date, 'time':time}, context_instance=RequestContext(request))


############################
#For Registering the Event #
############################

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['image'])  
      
      
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
    return HttpResponseRedirect('/events/success')
  else:
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
  return render_to_response(
    'events/register.html',
    variables
  )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})



