#!/bin/bash

docker exec -it spark-master bash -c "rm -rf /spark/stream"
docker cp . spark-master:/spark/stream
docker exec -it spark-master bash -c "spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 spark/stream/stream.py zoo:2181 radiation"
