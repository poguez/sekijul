from events.models import Event,EventImage
from django.contrib import admin
from django.contrib.admin import forms
from django.forms import ModelForm,Textarea

class ImageInline(admin.StackedInline):
  model = EventImage
  extra = 1 

class EventAdmin(admin.ModelAdmin,):
  fieldsets = [
    (None,			{'fields':['name']}),
    ('Date information',	{'fields':['date']}),
    ('General information',	{'fields':['place','rating','source','content','pub_date','user']}),
  ]
  inlines = [ImageInline]


# invalid line  widgets= {'content': Textarea(attrs={'cols': 80, 'rows': 20})}

admin.site.register(Event,EventAdmin)

