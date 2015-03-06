/home/vagrant/spark-1.2.0/bin/spark-submit \
        --class spark.elsa.OnlineSA \
        --master mesos://127.0.1.1:5050 \
        /home/vagrant/elsa/target/elsa-1.0-SNAPSHOT-jar-with-dependencies.jar \
        /home/vagrant/elsa/elsa.conf