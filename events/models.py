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
from django.contrib.auth.models import User


class Event(models.Model):
  name = models.CharField(max_length=200)
  date = models.DateTimeField('date of the event')
  place = models.CharField(max_length=200,blank=True)
  source = models.CharField(max_length=200,blank=True)
  content = models.CharField(max_length=3000, blank=True)
  rating = models.DecimalField(max_digits=6, decimal_places=5)
  pub_date = models.DateTimeField('date published')
  user = models.ForeignKey(User)  


  def was_published_today(self):
    return self.pub_date.date() == datetime.date.today()

  def __unicode__(self):
    return u'%s %s %s' % (self.id, self.name, self.place)

  def get_absolute_url(self):
    return "/events/%i/" % self.id

class EventImage(models.Model):
  event =  models.ForeignKey(Event)
  image = models.ImageField(blank=True,upload_to="media/photos")

  def __unicode__(self):
    return u"%s"  %  (self.image)
"""
class Rating(models.Model):
  event =  models.ForeignKey(Event)
"""
