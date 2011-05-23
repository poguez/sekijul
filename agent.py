# -*-coding: utf-8 -*-
import urllib
import urllib2
import sys
import re
import datetime
from BeautifulSoup import BeautifulSoup
from django.contrib.auth.models import User
from events.models import Event

def addNewEvent( date ):
    url = 'http://localhost:8080/events'
    postValue = {'pubdate_since':date}
    print 'Querying ', url, 'with', postValue


    data = urllib.urlencode(postValue)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    xml_data = unicode(response.read(), 'utf-8')
    soup = BeautifulSoup(xml_data)
    elems = soup.findAll('event')

    i = 0
    for elem in elems:
        """matchDate = re.match(r'(\d\d\d\d)/(\d?\d)/(\d?\d)', elem.find('date').string)
        print elem
        #print elem.date.string
        date = datetime.datetime(year = int(matchDate.group(1)),
                                 month = int(matchDate.group(2)),
                                day = int(matchDate.group(3)))
      #print date
        """        
        matchPubDate = re.match(r'(\d\d\d\d)/(\d?\d)/(\d?\d)', elem.find('pubdate').string)

        pubDate = datetime.datetime(year = int(matchPubDate.group(1)),
                                    month = int(matchPubDate.group(2)),
                                    day = int(matchPubDate.group(3)))

        # Extract and put in date, time, and place values
        # Date(year, month, day) value is always present.
        dateElem = elem.find('date')
        year = int(dateElem.find('year').string)
        month = int(dateElem.find('month').string)
        day = int(dateElem.find('day').string)
        date = datetime.date(year, month, day)

        # Time(hour, min) value is optional. But you won't notice it.
        timeElem = elem.find('time')
        if (timeElem) is not None:
          time = datetime.time(int(timeElem.find('hour').string),int(timeElem.find('min').string))
          dateAndTime = datetime.datetime.combine(date,time)
        else:
          time = datetime.time(0,0)
          dateAndTime = datetime.datetime.combine(date,time)
        # Place(just a string) value is optional. Be prepared for a None.
        place = "" 
        placeElem = elem.find('place')
        if (placeElem) is not None:
            place = placeElem.string
        if place is None:
            place = ""

#content =
	#print "asdfasdfasdfasdfadfad\n"
	#print  elem.content.div.renderContents()#find('content')#.string.replace(' clear=\"none\" ','')
	#contentString = ''
	#if(elem.content.div.string == None):
	  #Celeefind('div').string	 #unicode(elem.content.renderContents()),
	#  contentString = ''
	#else: 
       	contentString = elem.content.div.renderContents()  #unicode(elem.content.renderContents()),
        print contentString
	print contentString
	e = Event(name = elem.title.string,
                  date = dateAndTime,
                  content = contentString , #unicode(elem.content.renderContents()),
                  place = place, 
#                  image= u'',
                  pub_date = pubDate,
                  rating=0,
              source = elem.source.string,
              user=User.objects.get(username__exact='agent') )
        e.save()

        print 'Added to the Event table:', e
        i = i + 1

    print
    print i, 'events added. Danke schön'
