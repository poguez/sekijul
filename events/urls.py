from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    url(r'^(?P<event_id>\d+)/$', 'detail'),
    url(r'^$', 'index'),
    url(r'^new$', 'newPost'),
)


