from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from decimal import *
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets

class RegistrationForm(forms.Form):
  name = forms.CharField(label='name', max_length=200)
  date =  forms.DateTimeField(label='date')
  place = forms.CharField(label='place', max_length=200)
  source = forms.URLField(label='source',max_length=200)
  content = forms.CharField(widget=forms.TextInput(attrs={'size':'40','max_length':'3000'}))
  image =  forms.FileField(label='image')

