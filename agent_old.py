import urllib
import urllib2
import sys
import re
import datetime
from BeautifulSoup import BeautifulSoup

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
		
        matchDate = re.match(r'(\d\d\d\d)/(\d?\d)/(\d?\d)', elem.find('date').string)
        print elem
        #print elem.date.string
        date = datetime.datetime(year = int(matchDate.group(1)),
                                 month = int(matchDate.group(2)),
                                 day = int(matchDate.group(3)))
        #print date
        
        matchPubDate = re.match(r'(\d\d\d\d)/(\d?\d)/(\d?\d)', elem.find('pubdate').string)
        pubDate = datetime.datetime(year = int(matchPubDate.group(1)),
                                    month = int(matchPubDate.group(2)),
                                    day = int(matchPubDate.group(3)))
        
#content =
	#print "asdfasdfasdfasdfadfad\n"
	#print  elem.content.div.renderContents()#find('content')#.string.replace(' clear=\"none\" ','')
	contentString = ''
	if(elem.content.div.string == None):
	  #Celeefind('div').string	 #unicode(elem.content.renderContents()),
	  contentString = ''
	else: 
		contentString = elem.content.div.renderContents()  #unicode(elem.content.renderContents()),
		print contentString
	print contentString
	e = Event(name = elem.title.string,
                  date = date,
                  content = contentString , #unicode(elem.content.renderContents()),
                  place = elem.place.string, 
                  category= u'none',
                  image= u'',
                  pub_date = pubDate,
                  rating=0,
              source = elem.source.string)
        e.save()

        print 'Added to the Event table:', e
        i = i + 1

    print
    print i, 'events added. Danke sch?n'
