# -*-coding: utf-8 -*-
# ^ಠ_ಠ, Python
"""How to run
$ PYTHONPATH=BeautifulSoup-3.2.0 python2 manage.py shell
and invoke the function saveNewsprEvents(). Phew.
"""

import urllib2
from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import getDOMImplementation
import datetime
import re

from events.models import Event

newspr_url = 'http://newspr.kaist.ac.kr/boards/lst/perform/page:1'

def saveNewsprEvents():
  print 'Looking up', newspr_url
  print

  f = urllib2.urlopen(newspr_url)
  html_data = unicode(f.read(), 'utf-8')
  soup = BeautifulSoup(html_data)
  elems = soup.findAll('li', {"class":"news_list"})

  i = 0
  for elem in elems:
      print elem.findAll('dd')[1].contents[1]

      name = elem.findAll(['dt'])[0].strong.a.string
      place = elem.findAll('dd')[2].contents[1]
      date = elem.findAll('dd')[1].contents[1]

      print name, date, place
      dateMatch = re.match(r'(\d\d\d\d)-(\d\d)-(\d\d)', date)
      dateProper = datetime.datetime(year = int(dateMatch.group(1)),
                                     month = int(dateMatch.group(2)),
                                     day = int(dateMatch.group(3)))

      e = Event(name = name,
                date = dateProper,
                content = u"",
                place = place,
                image = u"",
                pub_date = datetime.datetime.today(),
                rating = 0,
                source = newspr_url)
      e.save()
      print 'Added to the Event table:', e
      i = i + 1

  print
  print i, u"events saved from newspr. Tack så myscket."
