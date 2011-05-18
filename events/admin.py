from events.models import Event
from django.contrib import admin
from django.contrib.admin import forms
from django.forms import ModelForm,Textarea

class EventAdmin(admin.ModelAdmin,):
  fieldsets = [
    (None,			{'fields':['name']}),
    ('Date information',	{'fields':['date']}),
    ('General information',	{'fields':['place','rating','image','source','content']}),
]
# invalid line  widgets= {'content': Textarea(attrs={'cols': 80, 'rows': 20})}

admin.site.register(Event,EventAdmin)

