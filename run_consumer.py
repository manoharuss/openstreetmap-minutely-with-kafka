from kafka import KafkaConsumer

if __name__ == "__main__":
    print("Running Consumer..")
    parsed_records = []
    topic_name = "openstreetmap-minutely"

    consumer = KafkaConsumer(
        topic_name,
        auto_offset_reset="earliest",
        bootstrap_servers=["localhost:9092"],
        api_version=(0, 10),
        consumer_timeout_ms=1000,
    )
    for published_msg in consumer:
        # This is the OpenStreetMap minutely osc text
        consume_text = published_msg.value
        # This is the sequenece number that belongs to the OpenStreetMap minutely diff
        consume_sequence = published_msg.key
        # TODO: We can do anything with the key/value pairs from here.
        print(f"Consumed sequence number {consume_sequence}")

    print("Consumer ended after reading all messages successfully.")

    consumer.close()
