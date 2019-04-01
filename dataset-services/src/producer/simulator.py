"""Module for kafka event producer"""

import numpy as np
import pandas as pd
import sys
import logging
import random
import string
import datetime
import src.config as config
from kafka import KafkaProducer
from json import dumps
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s-%(levelname)s-%(message)s',
                    filename='simulator.log',
                    filemode='w'
                    )

logger = logging.getLogger(__name__)

PUBLISH_DELAY_IN_SECONDS = 5
BOOTSTRAP_SERVERS = config.BOOTSTRAP_SERVERS
KAFKA_TOPIC = config.KAFKA_TOPIC


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def simulate(producer):
    """Simulate sample events for kafka"""

    # Sample restaurant names for review
    restaurant_names = ['BK Grill', 'Lucy Dinner Club', 'Pappa Grappa', 'Restaurant Gula Huset']
    while True:
        data = []
        x1 = np.random.randint(1, 5)
        x2 = datetime.datetime.now().strftime('%Y-%m-%d')
        x3 = np.random.choice(restaurant_names)
        x4 = random_string()
        data.append([x1, x2, x3, x4])
        df = pd.DataFrame(data)
        df.columns = ['stars', 'review_date', 'restaurant_name', 'user_id']
        for jdict in df.to_dict(orient='records'):
            producer.send(KAFKA_TOPIC, value=jdict)
            sleep(PUBLISH_DELAY_IN_SECONDS)


def main():
    try:
        logger.info("Starting kafka producer")
        producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))
        simulate(producer)
    except:
        e = sys.exc_info()[0]
        logger.error("Unable to simulate", exc_info=True)
    finally:
        producer.close()


if __name__ == '__main__':
    main()
