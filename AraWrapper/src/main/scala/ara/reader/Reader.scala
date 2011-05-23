package ara.reader

import scala.xml._
import dispatch._
import ara.datetime._

case class Article(title: String, pubDate: Date, source: String, html: NodeSeq, content: String)

object Reader {
  val credentials = Map("username"->"jjyoung", "password"->"jalapeno1")
  val araURL = "http://ara.kaist.ac.kr/"
}

class Reader {
  import Reader._
  import scala.collection.mutable.ListBuffer

  private val h = new Http()
  private val List(username, password, _*): List[String] = scala.io.Source.fromFile("credentials.txt").getLines().toList
  private val credentials = Map("username" -> username, "password" -> password)

  def read(since: Date) = {
    val loginPost = h(url(araURL + "account/login/") << credentials as_str)
    assert(loginPost.contains("MY INFO"), "Login failure")
    readFrom(since, 1).toList
  }
  private def readFrom(since: Date, page: Int): ListBuffer[Article] = {
    val query = if(page == 1) "" else "?page_no=" + page
    val listXML = loadXML("board/KAIST/" + query)

    val mainWrap = (listXML \ "body" \ "div").find(e => (e \ "@id").text == "mainWrap").get
    val contents = mainWrap \ "div" find (e => (e \ "@id").text == "contents") get
    val contentWrap = contents \ "div" find (e => (e \ "@class").text == "contentWrap") get 
    val board_content = contentWrap \ "div" find (e => (e \ "@id").text == "board_content") get
    val list = board_content \ "table" \ "tbody" \ "tr"

    def getDate(article: NodeSeq) = Date((article \ "td").find(e => (e \ "@class").text == "date").get.text)

    val articlesSince = new ListBuffer[Article]
    for (article <- list) {
      if (getDate(article) > since) {
	try {
	  val a = (article \ "td").find(e => (e \ "@class").text == "title").get \ "a"
	  articlesSince += readArticle((a \ "@href").text)
	} catch {
	  case ex: NoSuchElementException =>
	}
      }
    }
    if (getDate(list.last) > since) articlesSince ++ readFrom(since, page + 1)
    else articlesSince
  }

  private def loadXML(path: String) = {
    val string = h(url(araURL + path) as_str)

    val parserFactory = new org.ccil.cowan.tagsoup.jaxp.SAXFactoryImpl
    val parser = parserFactory.newSAXParser()
    val adapter = new scala.xml.parsing.NoBindingFactoryAdapter
    adapter.loadXML(
      new org.xml.sax.InputSource(
	new java.io.StringReader(string)), parser)
  }

  private def readArticle(path: String) = {
    val articleXML = loadXML(path)

    /* Scheiße, should've learned about implicits */
    val mainWrap= articleXML \ "body" \ "div" find (e => (e \ "@id").text == "mainWrap") get
    val contents = mainWrap \ "div" find (e => (e \ "@id").text == "contents") get
    val contentWrap = contents \ "div" find (e => (e \ "@class").text == "contentWrap") get
    val board_content = contentWrap \ "div" find (e => (e \ "@id").text == "board_content") get
    val articleView = board_content \ "div" find (e => (e \ "@class").text == "articleView") get
    val articleTitle = articleView \ "div" find (e => (e \ "@class").text == "articleTitle") get
    val articleContents = articleView \ "div" find (e => (e \ "@class").text == "articleContents") get
    val article = articleContents \ "div" find (e => (e \ "@class").text == "article") get

    val titleText = articleTitle \ "h3" \ "a" text
    val articleInfo = articleTitle \ "div" find (e => (e \ "@class").text == "articleInfo") get
    val dateText = ((articleInfo \ "p" find (e => (e \ "@class").text == "date") get) \ "a").text.takeWhile(_ != ' ')
    val pubDate = Date(dateText)
    
    val articleText = ("" /: article.child) ((x, y) => y match {
      case scala.xml.Text(s) => x + s.trim
      case <br></br> => x + "\n"
      case <a>{txt}</a> => x + txt.text
      case _ => x
    })
    Article(titleText, pubDate, araURL + path, article, articleText)
  }
}

