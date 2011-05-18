####################
#		   #
#   events-models  #
#		   #
####################

from django.db import models
import datetime
from decimal import *

#FORMS imports
from django.forms import ModelForm
from django import forms
import datetime
from django.forms.extras.widgets import SelectDateWidget

class Event(models.Model):
  name = models.CharField(max_length=200)
  date = models.DateTimeField('date of the event')
  place = models.CharField(max_length=200)
  source = models.CharField(max_length=200)
  content = models.CharField(max_length=3000)
  rating = models.DecimalField(max_digits=6, decimal_places=5)
  pub_date = models.DateTimeField('date published')
  image = models.ImageField(upload_to='event_img')

  def __unicode__(self):
#    return self.name
    return u'%s %s %s' % (self.id, self.name, self.place)
  def get_absolute_url(self):
    return "/events/%i/" % self.id


