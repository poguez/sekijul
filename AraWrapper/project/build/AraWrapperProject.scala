import sbt._

class AraWrapperProject(info: ProjectInfo) extends DefaultWebProject(info)
{
  val liftVersion = "2.3"
  lazy val hi = task { println("Hello World"); None }
  
  val jetty6 = "org.mortbay.jetty" % "jetty" % "6.1.14" % "test"  // jetty is only need for testing
  
  val dvers = "0.8.0"
  val http = "net.databinder" %% "dispatch-http" % dvers
  val nio = "net.databinder" %% "dispatch-nio" % dvers
}
