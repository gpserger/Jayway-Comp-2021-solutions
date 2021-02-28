package fettsidagen

import scala.collection._
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

    val people = readJSON("semlor.json")
        .filter(p => 
            ( p.preferences.wrap.toBoolean 
            ||p.preferences.glutenFree.toBoolean
            ||p.preferences.vegan.toBoolean
            ||p.preferences.chocolate.toBoolean
            ||p.preferences.regular.toBoolean
        ))
    
    // aaaaaaaaaaaaaaaaaahhhhhhhhhhhhhhhhh 
    val peopleNoSemla = readJSON("semlor.json")
    .filter(p => 
        !( p.preferences.wrap.toBoolean 
            ||p.preferences.glutenFree.toBoolean
            ||p.preferences.vegan.toBoolean
            ||p.preferences.chocolate.toBoolean
            ||p.preferences.regular.toBoolean
    ))
        
    val personSemla = mutable.Map[String, String]()
    
    case class Semla(name: String, var amount: Int)
    
    val semlor = Vector(
        Semla("regular", 100),
        Semla("chocolate", 50),
        Semla("vegan", 20),
        Semla("glutenFree", 15),
        Semla("wrap", 15)
    )

    def printAll: String = {
        // yea
        s"${personSemla.map(p => s"(${p._1}: ${p._2})").mkString(", ")}, ${peopleNoSemla.map(p => s"(${p.name.toString}: regular)").mkString(", ")}"
    }

    // "man ska inte använda return i scala"
    def findSemmelConsumer(i: Int): Boolean = {
        if (personSemla.size >= 197) return true
        else {
            for (x <- semlor.indices) {
                if (semlor(x).amount > 0 && people(i).preferences(semlor(x).name).toBoolean) {
                    personSemla += (people(i).name.toString -> semlor(x).name)
                    semlor(x).amount -= 1
                    if (findSemmelConsumer(i + 1)) return true
                    else {
                        personSemla -= (people(i).name.toString)
                        semlor(x).amount += 1
                    }
                }
            }
        }
        return false
    }
}

object Main extends App {
    println(ReadJSON.findSemmelConsumer(0))
    println(ReadJSON.printAll)
}