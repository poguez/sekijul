from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
  username = forms.CharField(label='Username', max_length=30)
  email = forms.EmailField(label='Email')
  password1 = forms.CharField(
     label='Password',
     widget=forms.PasswordInput()
  ) 
  password2 = forms.CharField(
     label='Password (Again)',
     widget=forms.PasswordInput()
  )  

def clean_password2(self):
  if 'password1' in self.clean_data:
    password1 = self.clean_data['password1']
    password2 = self.clean_data['password2']
    if password1==password2:
      return password2
    raise forms.ValidationError('Passwords are not the same.')

def clean_username(self):
  username = self.clean_data['username']
  if not re.search(r'^\w+$', username):
    raise forms.ValidationError('Username should only have alphanumeric characters and underscore.')
  try:
    User.objects.get(username=username)
  except ObjectDoesNotExist:
    return username
  raise forms.ValidationError('Username is already taken')

