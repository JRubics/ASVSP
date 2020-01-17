#!/usr/bin/python3
# 2015-01-01 01:00:00	2015	1	1	1	0	23	0	0	151.8	0	0	7	100.0

import os
from pyspark import SparkContext, SparkConf
import re

pattern = re.compile("\t")

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

conf = SparkConf().setAppName("projekat").setMaster("local")
sc = SparkContext(conf=conf)

# text_file = sc.textFile(HDFS_NAMENODE + "/projekat/mini.csv")
text_file = sc.textFile(HDFS_NAMENODE + "/projekat/dataset_batch.csv")
clouds = text_file \
    .flatMap(lambda line: line.replace(' ', '\t').split(" ")) \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .map(lambda line: (int(line.split()[13]), [float(line.split()[8]) / float(line.split()[11]), 1, float(line.split()[9]) / float(line.split()[12]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], [v[1][0]/v[1][1], v[1][2]/v[1][3]]))
clouds.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/clouds")

humidity = text_file \
    .flatMap(lambda line: line.replace(' ', '\t').split(" ")) \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .filter(lambda line: float(line.split()[13]) == 0) \
    .map(lambda line: (int(float(line.split()[14])), [float(line.split()[8]) / float(line.split()[11]), 1, float(line.split()[9]) / float(line.split()[12]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], [v[1][0]/v[1][1], v[1][2]/v[1][3]])) \
    .sortBy(lambda x: x[0])
humidity.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/humidity")

angle = text_file \
    .flatMap(lambda line: line.replace(' ', '\t').split(" ")) \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .map(lambda line: (int(float(line.split()[10])), [float(line.split()[8]) / float(line.split()[11]), 1, float(line.split()[9]) / float(line.split()[12]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], [v[1][0]/v[1][1], v[1][2]/v[1][3]])) \
    .sortBy(lambda x: x[0])
angle.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/angle")

# locations = text_file \
#     .flatMap(lambda line: line.replace(' ', '\t').split(" ")) \
#     .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0)
# locations.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/locations")

# .map(lambda line: (int(line.split()[13]), str(float(line.split()[8]) / float(line.split()[9])) + " " + str(float(line.split()[11]) / float(line.split()[12])))) \
# podeli u redove
# samo ako ima radijacije
# i kad je najjaca?
# vrsta oblaka, ghi, dhi, clratsky -||-
# suma, broj
# prosek

# ako nema oblaka kako utice vlaznost vazduha na odnos clearsky radijacije i radijacije
# kako ugao utice na radijaciju