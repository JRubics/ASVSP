#!/bin/bash
docker exec -it spark-master bash -c "apt update"
docker exec -it spark-master bash -c "apt install python -y"

docker exec -it spark-master bash -c "hdfs dfs -rm -r -f /data*"
docker exec -it spark-master bash -c "rm -rf /mapreduce"
docker cp . spark-master:/mapreduce
docker exec -it spark-master bash -c "chmod +x /mapreduce/map-reduce.sh && /mapreduce/map-reduce.sh"