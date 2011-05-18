from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from decimal import *

class RegistrationForm(forms.Form):
  name = forms.CharField(max_length=200)
  date =  forms.DateField(widget = SelectDateWidget())
  place = forms.CharField(max_length=200)
  source = forms.URLField()
  content = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
  image =  forms.FileField()
  pub_date = datetime.datetime.now()
  rating = Decimal(0)


def clean_username(self):
  username = self.clean_data['username']
  if not re.search(r'^\w+$', username):
    raise forms.ValidationError('Username should only have alphanumeric characters and underscore.')
  try:
    User.objects.get(username=username)
  except ObjectDoesNotExist:
    return username
  raise forms.ValidationError('Username is already taken')

