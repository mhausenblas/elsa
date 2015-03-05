# Elastic Sentiment Analysis (ElSA)


## What is this about?

The Elastic Sentiment Analysis (ElSA) is a simple Spark Streaming-based app that leverages the Mesos stack, esp. Marathon, to do the following:

* It takes a list of words (called topics in the following), such as *Mesos*, *Docker*, *DCOS*, etc., as input and, using the Twitter firehose, pulls tweets containing these topics for processing.
* Based on the tweet content it performs a simple sentiment per topic in an ongoing fashion. This ongoing operation is implemented via [Spark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html).
* Last but not least, based on the activity in a certain topic the app scales elastically through leveraging the [Marathon REST API](https://mesosphere.github.io/marathon/docs/rest-api.html). This means that if, for example, a rapid increase of mentions of the topic *DCOS* is detected (tweets per time unit), then more instances are launched.

## Dependencies

* Apache [Mesos 0.21.x](http://archive.apache.org/dist/mesos/0.21.0/) with [Marathon 0.7.6](https://github.com/mesosphere/marathon/releases/tag/v0.7.6)
* Apache [Spark 1.2.x](https://spark.apache.org/downloads.html)
* A Twitter account and an [app](https://apps.twitter.com/) that can be used for accessing the Twitter firehose

## Deployment

### Single node

### GCE

## Usage

TBD

## Notes

Apologies to all [Frozen](http://www.imdb.com/title/tt2294629/) fans, especially our kids, for hijacking the Elsa label in this context. I thought it's funny … 
