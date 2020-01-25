#!/bin/bash
DIR=/rdd

cd $DIR

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -mkdir /projekat
hdfs dfs -put dataset_test.csv  /projekat/

printf "\nRUN BATCH\n"

$SPARK_HOME/bin/spark-submit projekat.py

printf "\nSAVE RESULTS\n"
hdfs dfs -cat /projekat/result/clouds/* > results/clouds.txt
hdfs dfs -cat /projekat/result/humidity/* > results/humidity.txt
hdfs dfs -cat /projekat/result/angle/* > results/angle.txt
hdfs dfs -cat /projekat/result/temp/* > results/temp.txt

printf "\nPRINT RESULTS\n"

hdfs dfs -cat /projekat/result/clouds/*
hdfs dfs -cat /projekat/result/humidity/*
hdfs dfs -cat /projekat/result/angle/*
hdfs dfs -cat /projekat/result/temp/*
