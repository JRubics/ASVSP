#!/bin/bash
DIR=/mapreduce

cd $DIR

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -put dataset_0_-71_2015.csv /data

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_PREFIX

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /data \
    -output /data_out \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR/mapper.py \
    -file $DIR/reducer.py

printf "\nRESULTS\n"

hdfs dfs -cat /data_out/*