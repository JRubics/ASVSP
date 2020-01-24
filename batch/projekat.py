#!/usr/bin/python3

import os
from pyspark import SparkContext, SparkConf
import re

pattern = re.compile("\t")

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

conf = SparkConf().setAppName("projekat").setMaster("local")
sc = SparkContext(conf=conf)

# CLOUDS

cloud_names = {
    0: "clear",
    1: "probably_clear",
    2: "fog",
    3: "water",
    4: "supercooled_water",
    5: "mixed",
    6: "opaque_ice",
    7: "cirrus",
    8: "overlapping",
    9: "overshooting",
    10: "unknown",
    11: "dust",
    12: "smoke",
}

text_file = sc.textFile(HDFS_NAMENODE + "/projekat/dataset_batch.csv")

clouds = text_file \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .map(lambda line: (int(line.split()[13]), [float(line.split()[8]) / float(line.split()[11]), 1, float(line.split()[9]) / float(line.split()[12]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .sortBy(lambda x: x[0]) \
    .map(lambda v: "{0} {1} {2} {3}".format(v[0], cloud_names[v[0]], round(v[1][0] / v[1][1], 3), round(v[1][2] / v[1][3], 3)))
clouds.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/clouds")

# HUMIDITY

humidity = text_file \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .filter(lambda line: float(line.split()[13]) == 0) \
    .map(lambda line: (int(float(line.split()[14])), [float(line.split()[8]), 1, float(line.split()[9]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], v[1][0] / v[1][1], v[1][2] / v[1][3]))

max_dhi = humidity \
    .map(lambda x: x[1]) \
    .max()
max_dni = humidity \
    .map(lambda x: x[2]) \
    .max()

humidity = humidity \
    .sortBy(lambda x: x[0]) \
    .map(lambda v: "{0} {1} {2}".format(v[0], round(v[1] / max_dhi, 3), round(v[2] / max_dni, 3)))
humidity.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/humidity")

# ANGLE

angle = text_file \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .map(lambda line: (int(float(line.split()[10])), [float(line.split()[8]), 1, float(line.split()[9]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], v[1][0] / v[1][1], v[1][2] / v[1][3]))
# mora ponovo posto je sad drugaciji reduce
max_dhi = angle \
    .map(lambda x: x[1]) \
    .max()
max_dni = angle \
    .map(lambda x: x[2]) \
    .max()

angle = angle \
    .sortBy(lambda x: x[0]) \
    .map(lambda v: "{0} {1} {2}".format(v[0], v[1] / max_dhi, v[2] / max_dni))
angle.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/angle")

# TEMP

temp = text_file \
    .filter(lambda line: float(line.split()[8]) > 0 and float(line.split()[9]) > 0) \
    .map(lambda line: (int(float(line.split()[7])), [float(line.split()[8]), 1, float(line.split()[9]), 1])) \
    .reduceByKey(lambda a, b: [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]) \
    .map(lambda v: (v[0], round(v[1][0] / v[1][1], 3), round(v[1][2] / v[1][3], 3)))

max_dhi = temp \
    .map(lambda x: x[1]) \
    .max()
max_dni = temp \
    .map(lambda x: x[2]) \
    .max()

temp = temp \
    .sortBy(lambda x: x[0]) \
    .map(lambda v: "{0} {1} {2}".format(v[0], round(v[1] / max_dhi, 3), round(v[2] / max_dni, 3)))
temp.saveAsTextFile(HDFS_NAMENODE + "/projekat/result/temp")
