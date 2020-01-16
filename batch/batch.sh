#!/bin/bash
DIR=/rdd

cd $DIR

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -mkdir /projekat
hdfs dfs -put dataset_test.csv  /projekat/
# hdfs dfs -put mini.csv  /projekat/

printf "\nRUN BATCH\n"

$SPARK_HOME/bin/spark-submit projekat.py

printf "\nRESULTS\n"

hdfs dfs -cat /projekat/result/clouds/*
hdfs dfs -cat /projekat/result/humidity/*
hdfs dfs -cat /projekat/result/angle/*