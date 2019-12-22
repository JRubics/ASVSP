#!/usr/bin/python3

import os
from pyspark import SparkContext, SparkConf
import re

pattern = re.compile("\t")

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

conf = SparkConf().setAppName("projekat").setMaster("local")
sc = SparkContext(conf=conf)

text_file = sc.textFile(HDFS_NAMENODE + "/projekat/mini.csv")
counts = text_file.flatMap(lambda x: pattern.split(x)).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile(HDFS_NAMENODE + "/projekat/result")