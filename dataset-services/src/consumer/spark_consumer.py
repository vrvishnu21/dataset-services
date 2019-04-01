"""Module for Spark Streaming consumer"""

import json
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from src import config

import random
import datetime

# Loading properties from config
BOOTSTRAP_SERVERS = config.BOOTSTRAP_SERVERS
KAFKA_TOPIC = config.KAFKA_TOPIC

# Load DataType and Index for Elasticsearch
es_resource = "" + config.ES_INDEX + '/' + config.ES_TYPE

es_write_conf = {
    "es.resource": es_resource
}

def write_elastic_search(rdd):
    """Write events to ElasticSearch"""
    if rdd is None:
        return
    rdd.saveAsNewAPIHadoopFile(path='-',
                               outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
                               keyClass="org.apache.hadoop.io.NullWritable",
                               valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
                               conf=es_write_conf)



def generate_doc(item):
    """Generate document id"""
    dictinfo = json.loads(item)
    # add doc _id
    dictinfo["doc_id"] = str(random.randint(1, 1000000)) + ":" + datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S')
    result = (dictinfo["doc_id"], dictinfo)
    return result


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("DatasetConsumer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)

    # get streaming data from kafka
    kstream = KafkaUtils.createDirectStream(ssc, topics=[KAFKA_TOPIC],
                                            kafkaParams={"metadata.broker.list": BOOTSTRAP_SERVERS})

    # Extracting value from message tuple
    parsed_json = kstream.map(lambda x: x[1])

    # Generating document key
    new_record = parsed_json.map(lambda item: generate_doc(item))

    # Persist to elasticsearch
    new_record.foreachRDD(lambda rdd: write_elastic_search(rdd))

    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    main()
