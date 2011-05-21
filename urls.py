from django.conf.urls.defaults import *
from events import *
from django.contrib import admin
from django.contrib.comments.feeds import LatestCommentFeed
admin.autodiscover()
from django.views.generic.simple import direct_to_template

import os.path
from django.conf.urls.defaults import *

import settings

feeds = {
	'latest': LatestCommentFeed,
}

media = os.path.join(os.path.dirname(__file__), 'media')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls'),)
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #The main
    url(r'^$', 'views.main'),
    url(r'^events/', include('events.urls')),
    url(r'^comments/', include ('django.contrib.comments.urls')),
    
    # Comments feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds}),
    
    # This is the part from the login logout
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'views.logout_view'),
    url(r'^register/$', 'views.register_page'),
    url(r'^register/success/$', direct_to_template,{ 'template': 'registration/registration_success.html' }),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': media }),
)

