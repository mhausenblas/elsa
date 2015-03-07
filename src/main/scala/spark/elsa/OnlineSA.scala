package spark.elsa

import java.nio.file.{Paths, Files}
import java.nio.charset.StandardCharsets

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.twitter._

import org.streum.configrity._

object OnlineSA {

  def runAnalysis(elsaConf: Configuration): Unit = {

    // setting up the Spark configuration:
    val conf = new SparkConf().setAppName("ElSA Online").setMaster(elsaConf[String]("master"))
    // setting up the filename where to log the stats to:
    val stats = elsaConf[String]("stats-file")
    // setting up list of topics to be monitored by ElSA:
    val topics: Array[String] = elsaConf[String]("topics").split(",").distinct
    // setting up the Spark Streaming context:
    val ssc = new StreamingContext(conf, Seconds(elsaConf[Int]("batch-window")))

    // setting up system properties for Twitter4j lib OAuth credentials:
    System.setProperty("twitter4j.oauth.consumerKey", elsaConf[String]("consumer-key"))
    System.setProperty("twitter4j.oauth.consumerSecret", elsaConf[String]("consumer-secret"))
    System.setProperty("twitter4j.oauth.accessToken", elsaConf[String]("access-token"))
    System.setProperty("twitter4j.oauth.accessTokenSecret", elsaConf[String]("access-token-secret"))

    // sentiment triggers:
    val posSen: Array[String] = Array("like", "cool", "awesome", "nice", "good", "love")
    val negSen: Array[String] = Array("dislike", "meh", "bad", "sad", "hate", "mad")

    // hook into the Twitter firehose and get tweets with the topics of interest:
    val twitterFirehose = TwitterUtils.createStream(ssc, None, topics)


    twitterFirehose.foreachRDD(rdd => {
      val tweetCount = rdd.count()

      // overall stats:
      print("\n\nIn the past " + elsaConf[Int]("batch-window")  + " seconds " +
              "I found " + tweetCount + " tweet(s) " +
              "containing your topics: "
      )
      for (topic <- topics) print(topic + " ")
      println("\n**********************")

      // display tweet details and determine sentiment
      rdd.foreach{ tweet =>
        val tweetText = tweet.getText.toLowerCase // normalize for comparison with sentiments

        println("\n===\n" + tweetText + "\n===")

        // here comes the *very* simplistic sentiment analysis (just check if certain words are present):
        if ( posSen.exists(tweetText.contains) ) { print("SA: positive sentiment") }
        if ( negSen.exists(tweetText.contains) ) { print("SA: negative sentiment") }
      }

      // write out the tweet count as primary input for the auto-scale process:
      Files.write(Paths.get(stats), tweetCount.toString.getBytes(StandardCharsets.UTF_8))
    })

    // kick off the ongoing stream processing:
    //ssc.checkpoint(elsaConf[String]("checkpoint-dir"))
    ssc.start()
    ssc.awaitTermination()
  }

  def main(args: Array[String]) {
    if (args.length < 1) {
      System.err.println("Usage: OnlineSA  <config-file>")
      System.exit(1)
    }
    // setting up configuration:
    val elsaConf = Configuration.load(args(0))

    // makes sure that if and only if we're in production we don't show too verbose logs info:
    if (elsaConf[String]("deployment") == "production") {
      ElsaHelper.setLogLevel()
    }

    runAnalysis(elsaConf)
    System.exit(0)
  }
}