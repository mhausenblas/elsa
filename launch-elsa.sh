~/spark-1.2.0/bin/spark-submit \
  --class spark.elsa.OnlineSA \
  --master 127.0.0.1:5050 \
  target/elsa-1.0-SNAPSHOT-jar-with-dependencies.jar \
  elsa.conf