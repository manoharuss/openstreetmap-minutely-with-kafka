# openstreetmap-with-kafka 

This is an Apache Kafka implementation template to create a Producer and Consumer for listening to OpenStreetMap Minutely diffs.


## Install Kafka in machine

Let's download the latest Apache Kafka tar bundle and install it locally.

```sh
$ curl https://dlcdn.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz -o kafka_2.13-3.0.0.tgz
```


(At this point, we can move the kafka tar file into any directoy. The directory in which Kafka exists does not really have to be a specific path as long as a terminal session is running a Kafka session.)

Unzip the downloaded tar file and cd into the Kafka directory. 

```sh
$ tar -xzf kafka_2.13-3.0.0.tgz
$ cd kafka_2.13-3.0.0
```


### Start the ZooKeeper service from the local directory.

### Note: Soon, ZooKeeper may no longer be required by Apache Kafka in newer versions.

```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```


### Start Apache Kafka service

Open a new terminal session and start the Kafka broker service

```sh
$ bin/kafka-server-start.sh config/server.properties
```


✅ At this point, the required services for Apache Kafka have started. We can switch to running the code in this repository.


