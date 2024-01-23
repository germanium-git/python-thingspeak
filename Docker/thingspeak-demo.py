import thingspeak
import json
from datetime import datetime
import argparse


parser = argparse.ArgumentParser(description="input arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-k", "--api_key", help="Api key to talk to the channel")
parser.add_argument("-ch", "--channel_id", help="channel ID")

args = parser.parse_args()
config = vars(args)
# print(config)

# Instantiate the class Channel
ch = thingspeak.Channel(config["channel_id"],api_key=config["api_key"])

# Load the last result
channel_data = json.loads(ch.get({'results': 1}))

# Print the last value
print("The last value: ", (channel_data['feeds'][0]['field1']))

# Print the ID of the last value
print("The last value ID: ", (channel_data['feeds'][0]['entry_id']))

now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S')

data_to_update = {"field1": current_time}

# Update the channel with the current timestamp
ch.update(data_to_update)
