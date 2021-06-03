# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: UseCase123.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/24 14:57
# Desc:
# ------------------------------------------------------------------------------------------------
import os
import queue
import random

from genesis_blockchain_tools.contract import Contract
from genesis_blockchain_tools.crypto.backend.cryptography import sign, get_public_key
from locust import HttpLocust, TaskSequence, seq_task, between, task, TaskSet

from libs import api
from pftest001 import TestSystemContracts


class WebsiteTasks(TaskSet):

    @task
    def UseCase123(self):

        """
        大量转账交易，并且是长连接
        :return:
        """

        contract_name = 'UseCase123'

        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            # print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)

        # getuid

        token, uid, network_id = api.getuid(data["url"])
        print(token, network_id, uid)

        # login
        # pr_key = '3c8a5139eabb05e4c6bf2e0463af4c079458d839af779b3dd19fb2b0869ebca1'

        pr_key = data["pr_key"]
        signature = sign(pr_key, 'LOGIN' + network_id + uid)
        pubkey = get_public_key(pr_key)
        full_token = 'Bearer ' + token
        data1 = {
            'role_id': 0,
            'ecosystem': 1,
            'expire': 3600,
            'pubkey': pubkey,
            'signature': signature,
        }

        resp = self.client.post('/login', data=data1, headers={'Authorization': full_token})
        print("resp: {}".format( resp.json()))
        login_token = 'Bearer ' + resp.json()['token']
        print("actually login_token is {}".format(login_token))

        tx_data = {}
        headers = {}
        headers["Authorization"] = login_token
        for i in range(1, 2):
            redata = {"Comment": data["address"]}
            schema = api.contract(data["url"], login_token, contract_name)
            contract = Contract(schema=schema, private_key=pr_key, params=redata, ecosystem_id=1)
            tx_bin_data, txhash = contract.Multiconcat()
            tx_data[txhash] = tx_bin_data

        print(tx_data)
        resp = self.client.post('/sendTx', files=tx_data, headers=headers, name=contract_name)
        print(resp.text)


class WebsiteUser(HttpLocust):
    host = 'http://139.159.161.154:7079/api/v2'
    task_set = WebsiteTasks
    # 等待时间
    wait_time = between(5, 15)
    # print(TestSystemContracts().catche_read('wall50.txt', 'address'))
    queueData = queue.Queue()  # 队列实例化
    for count in range(16):
        data = {
            "url": ['http://139.159.161.154:7079/api/v2',
                    'http://139.159.244.108:7079/api/v2',
                    'http://139.9.105.233:7079/api/v2',
                    'http://124.71.10.27:7079/api/v2'
                    ][random.randint(0, 3)],
            # "url": host,
            "no": count,
            "pr_key": TestSystemContracts().catche_read('wall50.txt', 'pr_key')[count],
            "address": TestSystemContracts().catche_read('wall50.txt', 'address')[count],
        }
        print(data)
        queueData.put_nowait(data)


if __name__ == "__main__":
    host = 'http://139.159.161.154:7079/api/v2'  # node1

    # host = 'http://139.159.244.108:7079/api/v2'  # node2
    # host = 'http://139.9.105.233:7079/api/v2' #node3

    # os.system('locust -f gac_locust_run_slave3.py --slave')
    # os.system('locust -f gac_sendtokens.py')
    os.system('locust -f UseCase123.py --no-web -t 10s -c 1 -r 1')
