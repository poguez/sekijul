package ara.datetime

/*
 * dumb */
object Date {
  val date = """(\d\d\d\d)/(\d?\d)/(\d?\d)""".r
  def apply(year: Int, month: Int, day: Int) = new Date(year, month, day)
  def apply(s: String): Date = {
    val Date(year, month, day) = s
    Date(year, month, day)
  }
  def unapply(s: String) = {
    try {
      val date(year, month, day) = s
      Some(year.toInt, month.toInt, day.toInt)
    } catch {
      case _ => None
    }
  }
  def unapply(d: Date) = Some(d.year, d.month, d.day)
}
class Date(val year: Int, val month: Int, val day: Int) extends Ordered[Date] {
  def compare(that: Date) = {
    def chunk(d: Date) = d.year * 200 + d.month * 40 + d.day
    chunk(this) - chunk(that)
  }
  override def toString = year + "/" + month + "/" + day
}

/*
 * Just say NO to dumb codes! */
case class Time(hour: Int, min: Int) {
  override def toString =  hour + ":" + min
}
