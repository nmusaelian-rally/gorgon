import os
import time
import yaml
from pykafka import KafkaClient

def read_config(config_path):
    with open(config_path, 'r') as cf:
        content = cf.read()
        conf = yaml.load(content)
    return conf

def kafka():
    config = read_config('helpers/kafka_config.yml')
    kafka_home = config.get('KafkaHome')
    topic_name = config.get('TopicName')
    hosts = config.get('Hosts', 'localhost:9092')
    replication_factor = config.get('Replication', 1)
    partitions = config.get('Partitions', 1)
    zookeeper = config.get('Zookeeper', 'localhost:2181')
    kafka_client = KafkaClient(hosts=hosts)
    cmd = "%s/%s/bin/kafka-topics.sh" % (os.environ['HOME'], kafka_home)

    kafka_topic = kafka_client.topics[b'%s' % topic_name.encode()]
    if not kafka_topic:
        os.system("%s --create --zookeeper %s --replication-factor %s --partitions %s --topic %s"
                  % (cmd, zookeeper, replication_factor, partitions, topic_name))
    time.sleep(3)

    return kafka_topic.get_producer()