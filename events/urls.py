from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('events.views',
    url(r'^(?P<event_id>\d+)/$', 'detail'),
    url(r'^$', 'index'),
    url(r'^success$', direct_to_template,{'template':'events/registration_success.html'}),
    url(r'^/(?P<event_id>\d+)/vote/$', 'vote'),
    url(r'^search/', include('haystack.urls')),
    #url(r'^new$', 'register_page'),
)

