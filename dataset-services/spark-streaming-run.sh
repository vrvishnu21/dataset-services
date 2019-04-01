#!/bin/bash

# Download elasticsearch-hadoop dependencies
wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/6.7.0/elasticsearch-hadoop-6.7.0.jar

# Run spark consumer
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 \
             --jars elasticsearch-hadoop-6.7.0.jar \
             src/consumer/spark_consumer.py
