# Elastic Sentiment Analysis (ElSA)


## What is this about?

The Elastic Sentiment Analysis (ElSA) app leverages the Mesos stack, esp. Marathon to do the following:

* input is a list of topics such as *Mesos*, *Docker* or *DCOS*
* uses this seed list to hook into the Twitter firehose and pulls tweets tagged with these topics 
* based on the tweet content, generates word statistics per topic in an ongoing fashion, using [Spark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
* using [Marathon](https://mesosphere.github.io/marathon/) the app scales elastically, based on the activity in a certain topic (for example, if there are more mentions of the #IoT topic per time unit, more instances are launched)

## Dependencies

* Mesos and Marathon
* Spark
* Twitter account and create an [app](https://apps.twitter.com/˜)

## Deployment

TBD

## Usage

TBD

## Notes

Apologies to all [Frozen](http://www.imdb.com/title/tt2294629/) fans, especially our kids, for hijacking the Elsa label in this context. I thought it's funny … 
