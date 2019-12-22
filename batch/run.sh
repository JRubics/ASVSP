#!/bin/bash

docker exec -it spark-master bash -c "hdfs dfs -rm -r -f /projekat*"
docker exec -it spark-master bash -c "rm -rf /rdd"
docker cp . spark-master:/rdd
docker exec -it spark-master bash -c "chmod +x /rdd/batch.sh && /rdd/batch.sh"