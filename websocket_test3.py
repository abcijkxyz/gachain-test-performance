# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave2.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/24 14:57
# Desc:
# ------------------------------------------------------------------------------------------------
import time
import json
import asyncio
# from cent import generate_channel_sign
from centrifuge import Client, Credentials, CentrifugeException, PrivateSign
import logging
import requests
logger = logging.getLogger('centrifuge')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def run(loop):

    # Generate credentials.
    # In production this must only be done on backend side and you should
    # never show secret to client!
    headers = {'Content-Type': "application/json; charset=utf-8"}
    url = "https://node4.gachain.org:8900/api/websocket_token"
    data = {"head": {
            "version": "1.0",
            "msgtype": "request",
            "interface": "websocket_token",
            "remark": ""
            },

            "params": {
            "cmd": "001",
            "ecosystem": 1,
            "current_page": 1,
            "page_size": 10
            }
            }
    resp = requests.post(url, data=data, headers=headers)
    # print(resp.text)
    text = json.loads(str("{") + (resp.text.split('{')[-1]).split('}')[0] + str("}"))
    print(text)
    token = text["token"]
    address = text["url"]

    user = "1"
    timestamp = str(int(time.time()))
    info = json.dumps({"first_name": "Python", "last_name": "Client"})

    credentials = Credentials(user, timestamp, info, token)

    @asyncio.coroutine
    def connect_handler(**kwargs):
        print("Connected", kwargs)

    @asyncio.coroutine
    def disconnect_handler(**kwargs):
        print("Disconnected:", kwargs)

    @asyncio.coroutine
    def connect_error_handler(**kwargs):
        print("Error:", kwargs)

    client = Client(
        address, credentials,
        on_connect=connect_handler,
        on_disconnect=disconnect_handler,
        on_error=connect_error_handler,
    )

    yield from client.connect()

    @asyncio.coroutine
    def message_handler(**kwargs):
        print("Message:", kwargs)

    @asyncio.coroutine
    def join_handler(**kwargs):
        print("Join:", kwargs)

    @asyncio.coroutine
    def leave_handler(**kwargs):
        print("Leave:", kwargs)

    @asyncio.coroutine
    def subscribe_handler(**kwargs):
        print("Sub subscribed:", kwargs)

    @asyncio.coroutine
    def unsubscribe_handler(**kwargs):
        print("Sub unsubscribed:", kwargs)

    @asyncio.coroutine
    def error_handler(**kwargs):
        print("Sub error:", kwargs)

    sub = yield from client.subscribe(
        "public:1dashboard",
        on_message=message_handler,
        on_join=join_handler,
        on_leave=leave_handler,
        on_error=error_handler,
        on_subscribe=subscribe_handler,
        on_unsubscribe=unsubscribe_handler
    )

    try:
        success = yield from sub.publish({})
    except CentrifugeException as e:
        print("Publish error:", type(e), e)
    else:
        print("Publish successful:", success)

    try:
        history = yield from sub.history()
    except CentrifugeException as e:
        print("Channel history error:", type(e), e)
    else:
        print("Channel history:", history)

    try:
        presence = yield from sub.presence()
    except CentrifugeException as e:
        print("Channel presence error:", type(e), e)
    else:
        print("Channel presence:", presence)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        loop.close()
