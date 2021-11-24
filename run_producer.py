import requests
import tempfile
import gzip
from kafka import KafkaProducer


def get_sequence_number_url(sequence_number: int) -> str:
    # Given a sequence number, this method downloads the minutely diff file from planet.osm.org and returns the osc.gz file URL

    # Assert number of characters in the sequence_number is 7
    assert len(str(sequence_number)) == 7
    # When the number of characters in a sequence_number is 7, this is the way to create a osc file URL
    first_num = str(sequence_number)[0]
    second_num = str(sequence_number)[1:4]
    third_num = str(sequence_number)[4:7]

    url_construct = f"https://planet.osm.org/replication/minute/00{first_num}/{second_num}/{third_num}.osc.gz"
    return url_construct


def get_sequence_number_osc(url_construct: str) -> str:

    temp_file = tempfile.NamedTemporaryFile()
    response = requests.get(url_construct, stream=True)

    if response.status_code != 200:
        raise f"The URL for osc.gz file path may be wrong, a response code {response.status_code} is received."

    if response.status_code == 200:
        with open(temp_file.name, "wb") as f:
            f.write(response.raw.read())

    with gzip.open(temp_file, "rb") as f:
        osc_content_text = f.read().decode("utf-8")
        return osc_content_text


def connect_kafka_producer() -> KafkaProducer:
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"], api_version=(0, 10)
        )
    except Exception as ex:
        print("Exception while connecting Kafka and creating a Kafka Producer")
        print(str(ex))
    finally:
        return _producer


def publish_message(
    producer_instance: KafkaProducer, topic_name: str, key: str, value: str
) -> None:
    try:
        key_bytes = bytes(key, encoding="utf-8")
        value_bytes = bytes(value, encoding="utf-8")
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print("Message published successfully.")
    except Exception as ex:
        print("Exception in publishing message")
        print(str(ex))


# Check for minutely state


def get_remote_sequence_numbers() -> int:
    # Download the latest remote sequence number
    remote_latest_state = requests.get(
        "https://planet.osm.org/replication/minute/state.txt"
    )
    remote_sequencenumber_line = remote_latest_state.text.splitlines()[1]
    remote_sequence_number = int(remote_sequencenumber_line.split("sequenceNumber=")[1])
    return remote_sequence_number


def get_local_sequence_numbers() -> int:
    try:
        # Read the latest local sequence number if available
        local_latest_state = open("state.txt", "r")
        local_sequencenumber_line = local_latest_state.read().splitlines()[1]
        local_sequence_number = int(
            local_sequencenumber_line.split("sequenceNumber=")[1]
        )
        return local_sequence_number
    except:
        raise " No local state.txt available!! An initial state.txt is required."


def overwrite_local_sequence_number(sequence_number: int) -> None:

    # Assert number of characters in the sequence_number is 7
    assert len(str(sequence_number)) == 7
    # When the number of characters in a sequence_number is 7, this is the way to create a osc file URL
    first_num = str(sequence_number)[0]
    second_num = str(sequence_number)[1:4]
    third_num = str(sequence_number)[4:7]

    url_construct = f"https://planet.osm.org/replication/minute/00{first_num}/{second_num}/{third_num}.state.txt"

    remote_state = requests.get(url_construct)
    with open("state.txt", "w") as file:
        file.write(remote_state.text)

    return


if __name__ == "__main__":

    local_sequence_number = get_local_sequence_numbers()
    remote_sequence_number = get_remote_sequence_numbers()

    if local_sequence_number != remote_sequence_number:
        osc_gz_url = get_sequence_number_url(remote_sequence_number)
        osc_str = get_sequence_number_osc(osc_gz_url)
        # TODO: We can add more code to parse osc text into a JSON file using osmium tool
        # We can do something like
        # osmium export data.osm.pbf -o data.geojsonseq -c export-config.json
        # See https://docs.osmcode.org/osmium/latest/osmium-export.html for details
        print("Publishing minutely osc diff..")
        print(f"Publishing minutely sequence number : {remote_sequence_number}")

        # Create a Kafka producer
        producer = connect_kafka_producer()
        publish_message(
            producer, "openstreetmap-minutely", str(remote_sequence_number), osc_str
        )
        print(f"Publishing completed for sequence number : {remote_sequence_number}")

        # Now after successfully completing the publish, overwrite local state file
        overwrite_local_sequence_number(remote_sequence_number)
        print("Success!")

    else:
        # TODO: we need to sleep and rerun this producer every 1 minute at execution level
        pass
