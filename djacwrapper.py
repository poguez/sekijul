# -*-coding: utf-8 -*-
'''
Created on 2011. 4. 28.

@author: Dementor
'''
import urllib2
from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import getDOMImplementation
import re
import datetime
from django.contrib.auth.models import User

from events.models import Event

djac_url = 'http://djac.or.kr/html/kr/performance/performance_010101.html'
domain_url = 'http://djac.or.kr/'

def saveDjacEvents():
  print 'Looking up', djac_url
  print

  f = urllib2.urlopen(djac_url)
  html_data = unicode(f.read(), 'euc-kr')
  soup = BeautifulSoup(html_data)

  elems = soup.find('ul', id="schedulePerformance").findAll("li")

  i = 0
  for elem in elems:
      name = elem.find('dt').string
      place = elem.findAll('dd')[0].contents[1]
      date = elem.findAll('dd')[1].contents[1]
      img = elem.find('img', {'style':'width:123px'})['src']
      print "title, location, date triple start"
      print name + "|" +  date + "|" + place
      print "title, location, date triple end"

      dateMatch = re.search(ur'(\d\d\d\d)년 *(\d?\d)월 *(\d?\d)', date)
      if dateMatch is None:
          dateMatch = re.match(r'(\d\d\d\d)\. *(\d?\d)\. *(\d?\d)', date)
      dateProper = datetime.datetime(year = int(dateMatch.group(1)),
                                     month = int(dateMatch.group(2)),
                                     day = int(dateMatch.group(3)))

      e = Event(name = name,
                date = dateProper,
                content = u"",
                place = place,
                poster = domain_url + img,
                pub_date = datetime.datetime.today(),
                rating = 0,
                source = djac_url,
                user= User.objects.get(username__exact='agent'))
      e.save()
      print 'Added to the Event table:', e
      i = i + 1

  print
  print i, u"events saved from djac.or.kr. Muchas gracias."
