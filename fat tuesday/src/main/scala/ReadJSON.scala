package knattra

import scala.util.parsing.json._
import scala.io.Source
import JSON._

object ReadJSON {
    def readJSON(path: String) = {
        Source
            .fromFile(path)
            .getLines()
            .mkString
            .drop(1)
            .dropRight(1)
            .split("},")
            .map(i => s"$i}")
            .toVector
            .map(parseJSON)
    }
    
    //1 kolla alla med reg true och allt annat false
    //2 kolla alla med chocolate true och allt under falskt
    //3 kolla alla med vegan true och allt under falskt
    //4 kolla alla med glutenfree true och allt under falskt
    //5 kolla alla med wrap true

    val sortedReg = readJSON("semlor.json")
        .sortBy(person => person.preferences.wrap.toBoolean)
        .sortBy(person => person.preferences.glutenFree.toBoolean)
        .sortBy(person => person.preferences.vegan.toBoolean)
        .sortBy(person => person.preferences.chocolate.toBoolean)
        .sortBy(person => !person.preferences.regular.toBoolean)

    val sortedChoc = readJSON("semlor.json")
        .sortBy(person => person.preferences.regular.toBoolean)
        .sortBy(person => person.preferences.wrap.toBoolean)
        .sortBy(person => person.preferences.glutenFree.toBoolean)
        .sortBy(person => person.preferences.vegan.toBoolean)
        .sortBy(person => !person.preferences.chocolate.toBoolean)

    val sortedVeg = readJSON("semlor.json")
        .sortBy(person => person.preferences.chocolate.toBoolean)
        .sortBy(person => person.preferences.regular.toBoolean)
        .sortBy(person => person.preferences.wrap.toBoolean)
        .sortBy(person => person.preferences.glutenFree.toBoolean)
        .sortBy(person => !person.preferences.vegan.toBoolean)

    val sortedGlut = readJSON("semlor.json")
        .sortBy(person => person.preferences.vegan.toBoolean)
        .sortBy(person => person.preferences.chocolate.toBoolean)
        .sortBy(person => person.preferences.regular.toBoolean)
        .sortBy(person => person.preferences.wrap.toBoolean)
        .sortBy(person => !person.preferences.glutenFree.toBoolean)

    val sortedWrap = readJSON("semlor.json")
        .sortBy(person => person.preferences.glutenFree.toBoolean)
        .sortBy(person => person.preferences.vegan.toBoolean)
        .sortBy(person => person.preferences.chocolate.toBoolean)
        .sortBy(person => person.preferences.regular.toBoolean)
        .sortBy(person => !person.preferences.wrap.toBoolean)

    val itr: Vector[(String, Range, Vector[ScalaJSON])] = Vector(
        ("regular", (1 to 100), sortedReg),
        ("chocolate", (101 to 150), sortedChoc),
        ("vegan", (151 to 170), sortedVeg),
        ("glutenFree", (171 to 185), sortedGlut),
        ("wrap", (186 to 200), sortedWrap),
    )
            
    
    var points = 0
    
    for (i <- 0 until 100) if (sortedReg(i).preferences.regular.toBoolean) points += 1
    for (i <- 0 until 50)  if (sortedChoc(i).preferences.regular.toBoolean) points += 1
    for (i <- 0 until 20)  if (sortedVeg(i).preferences.regular.toBoolean) points += 1
    for (i <- 0 until 15)  if (sortedGlut(i).preferences.regular.toBoolean) points += 1
    for (i <- 0 until 15)  if (sortedWrap(i).preferences.regular.toBoolean) points += 1
}

object Main extends App {
    println(ReadJSON.points)
}