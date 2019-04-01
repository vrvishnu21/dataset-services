
# Dataset Services


## Introduction

The project tries to stream the sample dataset to a messaging queue and process the data using a real-time streaming program

## Project

There are two services.

simulator.py : generates the input data and push the event messages to kafka

spark_consumer.py : Stream the data from kafka and push to elasticsearch.

The config properties are defined in the config.py

Input:

Sample restaurant ratings are generated. Currently only the below columns are generated

| restaurant_name      | stars           |review_date    | user_id       |
| ---------------------| --------------- |-------------  | ------------- 
| Name of restaurant   |User's rating    |Date of review | User id       |
         
## Pre-requisites
Docker installed in the system

## Build

The project is dockerized. Navigate to the project directory and run the docker file to build the image.
This will take a while.

```
docker build -t bigdata .
```
where bigdata is the image name


## Execution

Once build is completed, the image will be created. Run the image to start the container.

```
docker run -it -d --rm --privileged -v `pwd`:/home/guest/host -p 23:22 -p 4040:4040 -p 5601:5601 -p 8888:8888 -p 9200:9200 -p 9300:9300 -p 2181:2181 -p 9092:9092 bigdata
```


To login to container via terminal

```
DOCKER_CONTAINER_ID=$(docker ps | grep bigdata | awk '{print $1}')

docker exec -it $DOCKER_CONTAINER_ID /bin/bash
```

## Install project dependencies
Once  logged in,you can find project files in the home folder. Now 
install the dependencies using pip.
```
pip install -r requirements.txt
```

## Run the streaming producer

This is a random data generator in python.

```
python src/producer/simulator.py

```

logs will be generated as simulator.log in the current directory.

Messages can be also viewed by running kafka
consumer

```
[root@949132e2e572 ~]# kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic reviews --from-beginning
{"stars": 2, "review_date": "2019-04-01", "restaurant_name": "Pappa Grappa", "user_id": "hfnxmhdasz"}
{"stars": 4, "review_date": "2019-04-01", "restaurant_name": "Restaurant Gula Huset", "user_id": "wdlgjjilrs"}
{"stars": 1, "review_date": "2019-04-01", "restaurant_name": "BK Grill", "user_id": "vhtvfkwiqq"}
```


## Run the streaming consumer

This is a pyspark program.


```
./spark-streaming-run.sh
```

Spark job can be monitored using spark ui

http://localhost:4040


## Output

Once job is running successfully, data will be continously persisted to elasticsearch. 
Using kibana ui, this can be verified and queried.

http://localhost:5601


