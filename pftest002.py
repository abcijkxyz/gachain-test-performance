# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: pftest002.py
# Author: Sect.Leuce
# Email: 812570241@qq.com
# Created: 2019/6/17 17:42
# Desc:
# ------------------------------------------------------------------------------------------------
import datetime
import random
from locust import HttpLocust, TaskSet, task
from libs import actions, tools, api
from genesis_blockchain_tools.contract import Contract
from pftest001 import TestSystemContracts
import queue
import os

class WebsiteTasks(TaskSet):

    '''def on_start(self):
        self.config = tools.read_config('nodes')
        #self.config = tools.read_config('main')
        #self.url = self.config[1]['url']
        #self.url = self.config['url']
        #self.pause = tools.read_config('test')['wait_tx_status']
        #self.pr_key = self.config[1]['private_key']
        #self.pr_key = self.config['private_key']
        #self.data = actions.login(self.url, self.pr_key, 0)
        #self.token = self.data['jwtToken']
        #keys = tools.read_fixtures('keys')
        #self.ldata = actions.login(self.config[1]['url'], keys['key2'], 0)'''

    @task
    def tokens_send(self):
        contract_name = 'TokensSend'
        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)
        # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
        print("url,pr_key", data["url"], data["pr_key"])
        token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
        print("token", token)
        # url = ["http://47.106.120.16:7079/api/v2","http://47.106.120.16:7079/api/v2"][random.randint(0, 1)]
        # pr_key = TestSystemContracts().catche_read('wall1.txt','pr_key')[random.randint(0, 10)]
        # token = actions.login(url, pr_key, 0)['jwtToken']

        schema = api.contract(data["url"],  token, contract_name)
        redata = {'Recipient': data["Recipient"], 'Amount': '100000000'}
        contract = Contract(schema=schema, private_key=data["pr_key"],
                            params=redata)
        tx_bin_data = contract.concat()
        self.client.post('/sendTx', files={'call1': tx_bin_data},
                         headers={'Authorization': token}, name=contract_name)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://node2.gachain.org:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(10):
        data = {
            # "url" :  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],

            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall1000.txt', 'pr_key')[random.randint(0, 100)],
            "Recipient": TestSystemContracts().catche_read('wall2000.txt', 'address')[random.randint(0, 100)],
        }
        queueData.put_nowait(data)
    # url = ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)]
    # pr_key = TestSystemContracts().catche_read('wall1.txt', 'pr_key')[random.randint(0, 10)]

    # token = actions.login(url, pr_key, 0)['jwtToken']

if __name__ == "__main__":
    os.system('locust -f pftest002.py')
