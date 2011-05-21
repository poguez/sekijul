################
#   views.py   #
#              #
################

from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from forms import * 
from events.models import Event

def main(request):
  latest_event_list = Event.objects.all().order_by('-pub_date')[:20]
  print latest_event_list
  variables = RequestContext(request,{
    'user':request.user,
    'latest_event_list':latest_event_list
  })
  
  return render_to_response('main_page.html',variables)

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password1'],
        email = form.cleaned_data['email']
      )
      print 'valid'
    return HttpResponseRedirect('/register/success')
  else:
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
  return render_to_response(
    'registration/register.html',
    variables
  )



