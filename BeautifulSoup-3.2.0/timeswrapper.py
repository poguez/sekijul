import urllib2
from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import getDOMImplementation

times_url = 'http://times.kaist.ac.kr/news/articleList.html?sc_section_code=S1N1'
impl = getDOMImplementation()

newdoc = impl.createDocument(None, "articles", None)
top_element = newdoc.documentElement

print 'Looking up', times_url
print

f = urllib2.urlopen(times_url)
html_data = unicode(f.read(), 'euc-kr')
soup = BeautifulSoup(html_data)
elems = soup.findAll('td',width="380",height="26",align="left")

for elem in elems:
    category = elem.findAll('span')[0].font.string
    title = elem.findAll('span')[1].a.font.string
    written_by = elem.parent.find('td', width="100", align="center").span.font.string
    date = elem.parent.find('td', width="80", align="center").span.font.string
    print category, title, written_by, date
    
    article = newdoc.createElement('article')
    top_element.appendChild(article)
    category_elem = newdoc.createElement('category')
    article.appendChild(category_elem)
    category_text = newdoc.createTextNode(category)
    category_elem.appendChild(category_text)
    title_elem = newdoc.createElement('title')
    article.appendChild(title_elem)
    title_text = newdoc.createTextNode(title)
    title_elem.appendChild(title_text)
    writtenby_elem = newdoc.createElement('writtenby')
    article.appendChild(writtenby_elem)
    writtenby_text = newdoc.createTextNode(written_by)
    writtenby_elem.appendChild(writtenby_text)
    date_elem = newdoc.createElement('date')
    article.appendChild(date_elem)
    date_text = newdoc.createTextNode(date)
    date_elem.appendChild(date_text)

xml_f_name = 'timeswrapper.xml'
xml_f = open(xml_f_name, 'w')
xml_f.write(newdoc.toprettyxml(indent="  ").encode('utf-8'))
xml_f.close()

print 'Produced an XML file named representing the results', xml_f_name


