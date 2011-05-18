
"""
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from decimal import *

class RegistrationForm(forms.Form):
  name = forms.CharField(label='name', x_length=200)
  date =  forms.DateField(label='date', widget = SelectDateWidget())
  place = forms.CharField(label='place', max_length=200)
  source = forms.URLField(label='source')
  content = forms.CharField(widget=forms.TextInput(label='content',attrs={'size':'40'}))
  image =  forms.FileField(label='image')
  pub_date = datetime.datetime.now()
  rating = Decimal(0)
"""
