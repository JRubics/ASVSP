r"""
 Run the example
    `$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/primeri/kafka_wordcount.py zoo:2181 subreddit-politics`
    `$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/primeri/kafka_wordcount.py zoo:2181 subreddit-politics subredit-funny`
"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
import math

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]


def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


def makeDict(clouds):
    dict = {}
    for i in range(len(clouds)):
       line = clouds[i].split()
       dict[int(line[0])] = [float(line[1]), float(line[2])]
    return dict


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="SparkStreamingKafkaWordCount")
    quiet_logs(sc)

    # clouds = sc.textFile(HDFS_NAMENODE + "/projekat/result/clouds").collect()
    # cloud_dict = makeDict(clouds)

    # clouds = {
    #     0: "clear",
    #     1: "probably_clear",
    #     2: "fog",
    #     3: "water",
    #     4: "supercooled_water",
    #     5: "mixed",
    #     6: "opaque_ice",
    #     7: "cirrus",
    #     8: "overlapping",
    #     9: "overshooting",
    #     10: "unknown",
    #     11: "dust",
    #     12: "smoke",
    # }
    # clouds[int(line.split()[13])]
    ssc = StreamingContext(sc, 3)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: "{0} {1}".format(x[0], x[1]))
    counts = lines.flatMap(lambda line: line.replace(' ', '\t').split(" ")) \
        .map(lambda line: "{0} {1} {2} {3}".format(line.split()[0], line.split()[1], round(float(line.split()[8]) + (float(line.split()[9]) * (math.cos(float(line.split()[10]) * math.pi / 180))), 3), "danger" if float(line.split()[8]) + (float(line.split()[9]) * (math.cos(float(line.split()[10]) * math.pi / 180))) > 800 else ""))

    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
