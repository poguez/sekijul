package ara

import javax.servlet.http.{HttpServlet,
			   HttpServletRequest => HSReq,
			   HttpServletResponse => HSResp}
import ara._
import ara.datetime._
import ara.reader._
import ara.extraction._
import scala.xml._

class AraWrapperServlet extends BaseServlet {
  def message() = {
    val ara = new Reader()
    val articles = ara.read(Date(param("pubdate_since")))
    val extracted = articles.map(a => (extract(a.content, a.pubDate), a.title, a.pubDate, a.source, a.html))
    <events>{
      for {((Some(Date(year, month, day)), time, place), title, pubDate, source, html) <- extracted}
      yield <event>
      <title>{title}</title>
      <date>
      <year>{year}</year>
      <month>{month}</month>
      <day>{day}</day>
      </date>
      {
	time match {
	  case Some(Time(hour, min)) =>
	    <time>
	  <hour>{hour}</hour>
	  <min>{min}</min>
	  </time>
	  case None => NodeSeq.Empty
	}
      }
      {
	place match {
	  case Some(placeText) =>
	    <place>{placeText}</place>
	  case None => NodeSeq.Empty
	}
      }
      <pubDate>{pubDate}</pubDate>
      <source>{source}</source>
      <content>{html}</content>
      </event>
    }
    </events>
  }
}

abstract class BaseServlet extends HttpServlet
{
  import scala.collection.mutable.{Map => MMap}
  
  def message : scala.xml.Node;
  
  protected var param : Map[String, String] = Map.empty
  protected var header : Map[String, String] = Map.empty
  
  override def doPost(req : HSReq, resp : HSResp) =
    {
      // Extract parameters
      //
      val m = MMap[String, String]()
      val e = req.getParameterNames()
      while (e.hasMoreElements())
      {
	val name = e.nextElement().asInstanceOf[String]
	m += (name -> req.getParameter(name))
      }
      param = Map.empty ++ m
      
      // Repeat for headers (not shown)
      //

      resp.setContentType("text/xml;charset=UTF-8")
      resp.getWriter().print(message)
    }
}

class NamedHelloWorldServlet extends BaseServlet {
  def message() =
    <html>
  <head><title>Hello, {param("disposition")} {param("name")}!</title></head>
  <body>Hey, {param("name")}, I heard that you are an {param("disposition")} fellow.
  is that true?</body>
  </html>
}
