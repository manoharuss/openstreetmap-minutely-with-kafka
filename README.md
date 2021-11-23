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

Open a new terminal session and create a Zookeeper session.

```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```


### Start Apache Kafka service

Open a new terminal session and start the Kafka broker service

```sh
$ bin/kafka-server-start.sh config/server.properties
```

### Start a Apache Kafka Topic and expose the Kafka Server through a local port number

Open a new terminal session and with below command, we create a new topic. Note that, at this point, we can rename the topic to any name. In this case, we are using openstreetmap-minutely as the topic name for example. 


Input parameters.
- Partition count: We also have to provide a partition count, in this example, I am choosing to give 10. Rule of thumb is to use partition count between 10-10000.
- Replication factor: Replication factor defines the number of distributed copies of a topic in a Kafka cluster. Replication factor can be defined at topic level and since this is an example repository that does not run on Cluster but only runs in a single node, I am using 1.


```sh
$ bin/kafka-topics.sh --create --topic openstreetmap-minutely --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1
```

```log
# Created topic openstreetmap-minutely.
```

✅ At this point, the required services for Apache Kafka have started. We can switch to running the code in this repository.


