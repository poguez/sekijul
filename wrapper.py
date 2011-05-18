import urllib2
from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import getDOMImplementation

times_url = 'http://newspr.kaist.ac.kr/boards/lst/perform/page:1'
impl = getDOMImplementation()

newdoc = impl.createDocument(None, "events", None)
top_element = newdoc.documentElement

print 'Looking up', times_url
print

f = urllib2.urlopen(times_url)
html_data = unicode(f.read(), 'utf-8')
soup = BeautifulSoup(html_data)
elems = soup.findAll('li', {"class":"news_list"})

for elem in elems:
    print elem.findAll('dd')[1].contents[1]
    
    name = elem.findAll(['dt'])[0].strong.a.string
    place = elem.findAll('dd')[2].contents[1]
    date = elem.findAll('dd')[1].contents[1]
    
    print name, place, date
    
    event = newdoc.createElement('event')
    top_element.appendChild(event)
    
    name_elem = newdoc.createElement('name')
    event.appendChild(name_elem)
    name_text = newdoc.createTextNode(name)
    name_elem.appendChild(name_text)
    

    
    place_elem = newdoc.createElement('place')
    event.appendChild(place_elem)
    place_text = newdoc.createTextNode(place)
    place_elem.appendChild(place_text)
    
    date_elem = newdoc.createElement('date')
    event.appendChild(date_elem)
    date_text = newdoc.createTextNode(date)
    date_elem.appendChild(date_text)

xml_f_name = 'newspr.xml'
xml_f = open(xml_f_name, 'w')
xml_f.write(newdoc.toprettyxml(indent="  ").encode('utf-8'))
xml_f.close()

print 'Produced an XML file named representing the results', xml_f_name


