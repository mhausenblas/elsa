~/bin/spark-1.2.0/bin/spark-submit \
  --class spark.elsa.OnlineSA \
  --master local[2] \
  target/elsa-1.0-SNAPSHOT-jar-with-dependencies.jar \
  elsa.conf