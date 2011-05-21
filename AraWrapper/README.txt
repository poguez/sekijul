Description
-----------

AraWrapper is a web service that serves events information available on http://ara.kaist.ac.kr/board/KAIST.

AraWrapper is implemented as a java servlet. It serves event information in XML format upon a POST request. A POST request should have a parameter, 'pubdate_since', setting the lower bound of published date regarding the event information the wrapper collects. A response is like this

<events>
  <event>
    <title>[학부총학생회] 혁신비상위원회 공청회 공지</title>
    <date>
      <year>2011</year>
      <month>5</month>
      <day>18</day>
    </date>
    <time>
      <hour>20</hour>
      <min>0</min>
    </time>
    <place>태울관 미래홀</place>
      <pubDate>2011/5/17</pubDate>
      <source>http://ara.kaist.ac.kr//board/KAIST/204716/?page_no=1</source>
      <content>
        <div class="article">
          학우 공청회: OMG U SHOULD TOTALLY COME SEE MY EVENT!!!1!
	</div>
     </content>
  </event>
</events>

The project is setup as an sbt(simple-scala-builder) project, so you want to use that(sbt) to build/run this thing. A quick procedure:
1. Install sbt. (Google Simple Scala Build)
2. cd to the AraWrapper project directory.
3. You need to provide ARA login credentials. Make a text file named credentials.txt in the project directory and make it include  ARA credentials in the following format.

username
password

Don't include any blank lines prior to username.
4. Run sbt.
5. Type in in the prompt 'update' (without quotes).
6. Run 'jetty-run'.
7. Make sure agent.py points to the correct IP/port.
8. Run agent.py
9. Eat nachos.