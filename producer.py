import requests

# Download the latest remote sequence number
remote_latest_state = requests.get('https://planet.osm.org/replication/minute/state.txt')
remote_sequencenumber_line = remote_latest_state.text.splitlines()[1]
remote_sequence_number = int(remote_sequencenumber_line.split('sequenceNumber=')[1])
print(remote_sequence_number)

# Download the latest local sequence number
local_latest_state = open("state.txt", "r")
local_sequencenumber_line = local_latest_state.read().splitlines()[1]
local_sequence_number = int(local_sequencenumber_line.split('sequenceNumber=')[1])
print(local_sequence_number)

# Compare the 2 states and if they do not match, return mismatch
if remote_sequence_number != local_sequence_number:
    print("mismatch")

