# # /usr/bin/python
# # -*- coding:UTF-8 -*-
#
from cent import Client

url = "https://node4.gachain.org:10091"
api_key = "5872a29c-25d3-45d8-b6f2-0b36c44407cd"

# initialize client instance.
client = Client(url, api_key=api_key, timeout=1)

# publish data into channel
channel = "public:chat"
data = {"input": "test"}
client.publish(channel, data)

# other available methods
client.unsubscribe("USER_ID")
client.disconnect("USER_ID")
messages = client.history("public:chat")
clients = client.presence("public:chat")
channels = client.channels()
stats = client.info()
client.history_remove("public:chat")