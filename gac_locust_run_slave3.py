# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave3.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/26 9:57
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
import time
from genesis_blockchain_tools.crypto import sign
from genesis_blockchain_tools.crypto import get_public_key
import json


class WebsiteTasks(TaskSet):

    @task
    def tokens_send(self):
        """
        转账
        :return:
        """
        contract_name = 'TokensSend'
        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            # print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)

        # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
        print("actually slave3 url pr_key token is {} and {}".format(data["url"], data["pr_key"], data["token"]))
        print("actually slave3 Recipient is {}".format(data["Recipient"]))
        login_token = data["token"]

        # print('get login_token url is {} and {}'.format(login_token, data["url"]))
        schema = api.contract(data["url"],  login_token, contract_name)
        redata = {'Recipient': data["Recipient"], 'Amount': '1'}
        contract = Contract(schema=schema, private_key=data["pr_key"],
                            params=redata)
        tx_bin_data = contract.concat()
        resp = self.client.post('/sendTx', files={'call1': tx_bin_data},
                                headers={'Authorization': login_token}, name=contract_name)
        print(resp.text)
        # hash = json.loads(resp.text)["hashes"]["call1"]
        # # print(hash)
        # resp_p = api.tx_status(data["url"], token, hash)
        # print("转账结果：%s" % resp_p)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://3.1.66.88:7079/api/v2"
    # host = "http://127.0.0.1:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(2000):
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],

            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('token10.txt', 'pr_key')[count],
            "token": TestSystemContracts().catche_read('token10.txt', 'token')[count],
            "Recipient": TestSystemContracts().catche_read('wall1000.txt', 'address')[random.randint(0, 500)]
        }
        # print(data)
        queueData.put_nowait(data)


if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave3.py --slave')
    os.system('locust -f gac_locust_run_slave3.py')
    # os.system('locust -f gac_locust_run_slave3.py --no-web -c 1 -r 1')
