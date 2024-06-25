
ThisBuild / scalaVersion     := "2.12.12"
ThisBuild / version          := "0.1.0"
ThisBuild / organization     := "edu.ucsc.cse"

lazy val root = (project in file("."))
  .settings(
    name := "chisel_regression",
    libraryDependencies ++= Seq(
      "edu.berkeley.cs" %% "chisel3" % "3.5.0-RC2",
      "edu.berkeley.cs" %% "chiseltest" % "0.3.2" % "test"
    ),
    scalacOptions ++= Seq(
      "-Xsource:2.11",
      "-language:reflectiveCalls",
      "-deprecation",
      "-feature",
      "-Xcheckinit"
    ),
    addCompilerPlugin("edu.berkeley.cs" % "chisel3-plugin" % "3.6.1" cross CrossVersion.full),
    addCompilerPlugin("org.scalamacros" % "paradise" % "2.1.1" cross CrossVersion.full)
  )

