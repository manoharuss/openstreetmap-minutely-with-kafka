# openstreetmap-minutely-with-kafka 

This is an Apache Kafka implementation template to create a Producer and Consumer for listening to OpenStreetMap Minutely diffs. Each Pub/Sub message is a minutely osc.gz text, we can further break this down into a single geojson by parsing the osc file with [osmium-tool](https://docs.osmcode.org/osmium/latest/osmium-export.html).

- [Installation](#installation)
  - [Install Kafka in machine](#install-kafka-in-machine)
  - [Start the ZooKeeper service](#start-the-zookeeper-service)
  - [Start the Kafka service](#start-the-kafka-service)
  - [Start a Kafka Topic and expose the bootstrap Server through a localport](#start-a-kafka-topic-and-expose-the-bootstrap-server-through-a-localport)
  - [Inspect messages](#inspect-messages)
  - [Run producer](#run-producer)
  - [Run Consumer](#run-consumer)




# Installation

## Install Kafka in machine

Let's download the latest Apache Kafka tar bundle and use it locally.

```sh
curl https://dlcdn.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz -o kafka_2.13-3.0.0.tgz
```


(At this point, we can move the kafka tar file into any directoy. The directory in which Kafka exists does not really have to be a specific path as long as a terminal session is running a Kafka session.)

Unzip the downloaded tar file and cd into the Kafka directory. 

```sh
tar -xzf kafka_2.13-3.0.0.tgz
```

Go into the kafka package directory to start the services.

```sh
cd kafka_2.13-3.0.0
```


## Start the ZooKeeper service

### Note: Soon, ZooKeeper may no longer be required by Apache Kafka in newer versions.

Since Kafka runs on Zookeeper, we need to start the Zookeeper service in the background in a terminal session. Open a new terminal session and create a Zookeeper session with below command.

```sh
bin/zookeeper-server-start.sh config/zookeeper.properties
```


## Start the Kafka service

Similarly, open a new terminal session and start the Kafka broker service.

```sh
bin/kafka-server-start.sh config/server.properties
```

## Start a Kafka Topic and expose the bootstrap Server through a localport

Open a new terminal session and with below command, we can create a new topic. Note that, at this point, we can rename the topic to any name. In this case, we are using openstreetmap-minutely as the topic name for example. 


Required input parameters.
- Partition count: We also have to provide a partition count, in this example, I am choosing to give 10. Rule of thumb is to use partition count between 10-10000.
- Replication factor: Replication factor defines the number of distributed backup copies of a topic in a Kafka cluster. Replication factor can be defined at topic level and since this is an example repository that does not run on Cluster but only runs in a single node, I am using 1.


```sh
bin/kafka-topics.sh --create --topic openstreetmap-minutely --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1
```

A successful creation of a topic returns a log output like below.
```log
# Created topic openstreetmap-minutely.
```

✅ At this point, the required zookeeper and Kafka broker service have started and we also created a topic. We can switch to running Producer and Consumer code in this repository.


## Inspect messages

To inspect messages, we can console out all the messages published into the topic since the beginning.

```sh
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic openstreetmap-minutely --from-beginning
```


# Run producer

After the Kafka services have started and a topic name is created, we can now publish messages into the topic.

In `run_producer.py`, we have a sample code that downloads and keeps state of every openstreetmap minutely file. If there is a new state.txt change, the osc.gz file is downloaded and published as a new message.

**Try it locally**

```sh
python run_producer.py
```

When there is a new minutely file and the sequence number than the state.txt committed to the repo, the producer code will publish osc text file.

```log
Publishing minutely osc diff..
Publishing minutely sequence number : 4815209
Message published successfully.
Publishing completed for sequence number : 4815209
Success!
```


# Run Consumer

Once few messages are published, a consumer app can download the published messages and run business logic with those messages.

We can have a consumer run and Subscribe to messages published from the very beginning. Try running the consumer after publishing few messages.

```sh
python run_consumer.py
```

When there are messages, the consumer will log out all the sequence numbers to terminal for verification.

```log
Running Consumer..
Consumed sequence number b'4815169'
Consumed sequence number b'4815208'
Consumed sequence number b'4814390'
Consumed sequence number b'4814387'
Consumed sequence number b'4814389'
Consumed sequence number b'4815209'
Consumer ended after reading all messages successfully.
```

