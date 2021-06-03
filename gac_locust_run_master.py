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

    # @task
    # def register_login(self):
    #     """
    #     新用户注册登录
    #     :return:
    #     """
    #     try:
    #         data = self.locust.queueData.get()
    #         self.locust.queueData.put_nowait(data)
    #         # print(data)
    #     except queue.Empty:
    #         print('no data exist')
    #         exit(0)
    #     # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
    #     print("actually slave1 pr_key is {}".format(data["pr_key"]))
    #     token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']

    # @task(1)
    # def tokens_send(self):
    #     contract_name = 'TokensSend'
    #     try:
    #         data = self.locust.queueData.get()
    #         self.locust.queueData.put_nowait(data)
    #         # print(data)
    #     except queue.Empty:
    #         print('no data exist')
    #         exit(0)
    #     # print("url,pr_key",data["url"], data["pr_key"])
    #     token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
    #     # print("token",token)
    #     # actions.tx_status(data["url"],60)
    #     schema = api.contract(data["url"],  token, contract_name)
    #     redata = {'Recipient': data["Recipient"], 'Amount': '1000000000000'}
    #     contract = Contract(schema=schema, private_key=data["pr_key"],
    #                         params=redata)
    #     tx_bin_data = contract.concat()
    #     self.client.post('/sendTx', files={str(): tx_bin_data},
    #                      headers={'Authorization': token}, name=contract_name)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    # # host = "http://127.0.0.1:7079/api/v2"
    # host = "https://node1.gachain.org:7079/api/v2"
    # queueData = queue.Queue()  # 队列实例化
    # for count in range(100):
    #     data = {
    #         "no": count,
    #         "url": host,
    #         "pr_key": TestSystemContracts().catche_read('wall1000.txt', 'pr_key')[count],
    #         "Recipient": TestSystemContracts().catche_read('wall2000.txt', 'address')[random.randint(0, 100)],
    #     }
    #     # print("actually pr_key is {}".format(data["pr_key"]))
    #     queueData.put_nowait(data)

if __name__ == "__main__":
    os.system('locust -f gac_locust_run_master.py --master')

