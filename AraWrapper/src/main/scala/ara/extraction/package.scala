package ara

package object extraction {
  import ara.datetime._
  private val year = """\d\d\d\d""".r
  private val month, day, hour, min = """\d?\d""".r
  private val min24 = """\d\d""".r
  private val am = """오전|낮|am""".r
  private val pm = """밤|저녁|오후|점심|늦은|pm""".r
  private val dateDetail1 = (".*?(?:(" + year + ")/)?(" + month + ")/(" + day + ").*").r
  private val dateDetail2 = (".*?(?:(" + year + """)\.)? *(""" + month + """)\. *(""" + day + ").*").r
  private val dateDetail3 = (".*?(?:(" + year + ")년)? *(?:(" + month + ")월)? *(" + day + """)(?: *~ *\d?\d)?일.*""").r
  private val dateDetail4 = (".*(오늘|금일).*").r
  private val timeDetail1 = (".*?(" + hour + ")시 *(?:(" + min + ")분)?.*").r
  private val timeDetail2 = (".*?(" + hour + "):(" + min24 + ").*").r

  private def saneDate(year: String, month: String, day: String) = {
    val saneYear = if (year != null) {
      val y = year.toInt
      y >= 1988 && y <= 2100
    } else true
    val saneMonth = if (month != null) {
      val m = month.toInt
      m >= 1 && m <= 12
    } else true
    val saneDate = day.toInt >= 1 && day.toInt <= 31
    saneYear && saneMonth && saneDate
    // This code is not sane.
  }

  private def dateDetail(f: String, pubDate: Date) = f match {
    case dateDetail1(year, month, day) if saneDate(year, month, day) =>
      Some(Date(if (year == null) pubDate.year else year.toInt, month.toInt, day.toInt))
    case dateDetail2(year, month, day) if saneDate(year, month, day) =>
      Some(Date(if (year == null) pubDate.year else year.toInt, month.toInt, day.toInt))
    case dateDetail3(year, month, day) if saneDate(year, month, day) =>
      Some(Date(if (year == null) pubDate.year else year.toInt, if (month == null) pubDate.month else month.toInt, day.toInt))
    case dateDetail4(today) => Some(pubDate)
    case _ => None
  }

  private def saneTime(hour: String, min: String) = {
    val saneHour = hour.toInt >= 0 && hour.toInt <= 23
    val saneMin = if (min != null) {
      val m = min.toInt
      m >= 0 && m <= 59
    } else true
    saneHour && saneMin
  }

  private def timeDetail(f: String) = f match {
    case timeDetail1(hour, min) if saneTime(hour, min) => {
      val h = hour.toInt
      val m = if (min != null) {
	min.toInt
      } else {
	0
      }
      if (am.findFirstIn(f) != None) {
	// What is remain of what has so far been my train of thought is nothing more than a smoking wreckage and a mountain of soda canisters.
	Some(Time(h, m))
      } else if (pm.findFirstIn(f) != None) {
	// Varning: Den där koden fungerar inte.
	// En annan varning: Jag kan inte tala svenska.
	Some(Time(if (h <= 11) h + 12 else h, m))
      } else if (h >= 13) {
	Some(Time(h, m))
      } else { None }
    }
    case timeDetail2(hour, min) if saneTime(hour, min) =>
      Some(Time(hour.toInt, min.toInt))
    case _ => None
  }

  private def extractFormatted(article: String, pubDate: Date) = {
    val temporalSig = """일시|일 시|기간|시기|시간|date|time""".r
    val placeSig = """장소|장 소|place""".r

    val fragments = article.lines.map(_.span(_ != ':')).filter(_._2 != "")
    val temporalFrag = fragments.find{case (s, _) => temporalSig.findFirstIn(s) != None}.map(_._2.tail)

    val placeDetail = fragments.find{case (s, _) => placeSig.findFirstIn(s) != None}.map(_._2.tail.trim)

    val date = temporalFrag match {
      case None => None
      case Some(f) => dateDetail(f, pubDate)
    }
    val time = temporalFrag match {
      case None => None
      case Some(f) => timeDetail(f)
    }
    (date, time, placeDetail)
  }

  private def extractNatural(article: String, pubDate: Date) = {
    def sentences(s: String): List[String] = {
      val endOfSentenceMarkers = """(다.|다!|다~)""".r
      endOfSentenceMarkers.findFirstMatchIn(s) match {
	case None => List(s)
	case Some(m) => m.before + m.matched :: sentences(m.after.toString)
      }
    }

    def phrases(s: String): List[String] = {
      val phrasalMarkers = """(가|이|를|을|에|로|으로|부터|동안|까지|,|~)\s+""".r
      phrasalMarkers.findFirstMatchIn(s) match {
	case None => List(s)
	case Some(m) => m.before + m.matched :: phrases(m.after.toString)
      }
    }
    def findDetail(ss: List[String]): (Option[Date], Option[Time], Option[String]) = {
      val temporalPhrasalMarkers = """(에|부터|동안|까지|,|~)\s+\z""".r
      val spatialPhrasalMarkers = """(에서)""".r
      def findTemporalDetailPhrasal(ps: List[String]): (Option[Date], Option[Time]) = ps match {
	case Nil => (None, None)
	  case p :: rest => temporalPhrasalMarkers.findFirstMatchIn(p) match {
	    case None => findTemporalDetailPhrasal(rest)
	    case Some(m) =>
	      (dateDetail(m.before.toString, pubDate), timeDetail(m.before.toString)) match {
		case (date @ Some(_), time) => (date, time)
		case _ => findTemporalDetailPhrasal(rest)
	      }
	  }
      }
      def findSpatialDetailPhrasal(ps: List[String]): Option[String] = ps match {
	case Nil => None
	case p :: rest => spatialPhrasalMarkers.findFirstMatchIn(p) match {
	  case None => findSpatialDetailPhrasal(rest)
	  case Some(m) => Some(m.before.toString.trim)
	}
      }
      ss match {
	case Nil => (None, None, None)
	  case s :: rest => findTemporalDetailPhrasal(phrases(s)) match {
	    case (None, _) => findDetail(rest)
	    case (date @ Some(_), time) => findSpatialDetailPhrasal(phrases(s)) match {
	      case None => findDetail(rest)
	      case place @ Some(_) => (date, time, place)
	    }
	  }
      }
    }
    findDetail(sentences(article))
  }

  def extract(article: String, pubDate: Date) = extractFormatted(article, pubDate) match {
    case (date @ Some(_), time, place) => (date, time, place)
    case _ => extractNatural(article, pubDate)
  }
}
