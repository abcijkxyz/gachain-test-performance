# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave2.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/24 14:57
# Desc:
# ------------------------------------------------------------------------------------------------
from locust import Locust, events, task, TaskSet
import websocket
import time
import gzip


class WebSocketClient():
    def __init__(self, host):
        self.host = host

        # self.port = port


class WebSocketLocust(Locust):
    def __init__(self, *args, **kwargs):
        self.client = WebSocketClient("172.16.218.123")


class UserBehavior(TaskSet):
    # ws = websocket.WebSocket()
    # #self.ws.connect("ws://10.98.64.103:8807")
    # ws.connect("ws://pro-web-new.devtest.exshell-dev.com/r1/main/ws")

    @task(1)
    def buy(self):

        try:
            ws = websocket.WebSocket()
            # self.ws.connect("ws://10.98.64.103:8807")
            ws.connect("wss://node4.gachain.org:10091/connection/websocket")
            start_time = time.time()
            # self.ws.send('{"url":"/buy","data":{"id":"123","issue":"20170822","doubled_num":2}}')
            # result = self.ws.recv()

            send_info = '{"sub": "1dashboard"}'
            # send_info = '{"event":"subscribe", "channel":"btc_usdt.deep"}'
            while True:
                # time.sleep(5)
                # ws.send(json.dumps(send_info))
                ws.send(send_info)
                while (1):
                    compressData = ws.recv()
                    result = gzip.decompress(compressData).decode('utf-8')
                    if result[:7] == '{"ping"':
                        ts = result[8:21]
                        pong = '{"pong":' + ts + '}'
                        ws.send(pong)
                    ws.send(send_info)
                    # else:
                    #     # print(result)
                    #     with open('./test_result.txt', 'a') as f:
                    #         #f.write(threading.currentThread().name + '\n')
                    #         f.write(result + '\n')

        except Exception as e:
            print("error is:", e)


class ApiUser(WebSocketLocust):
    task_set = UserBehavior

    min_wait = 100

    max_wait = 200
