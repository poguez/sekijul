import datetime
from haystack import indexes
from events.models import Event

class EventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')
    place = indexes.CharField(model_attr='place')
    rating = indexes.DecimalField(model_attr='rating')

    def get_model(self):
        return Event
