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
        大量转账交易，并且是长连接
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
        print("actually slave3 url pr_key Recipient is {} and {}".format(data["url"], data["pr_key"], data["Recipient"]))
        token, uid, network_id = api.getuid(data["url"])
        # print("actually token, uid, network_id is {} and {}".format(token, uid, network_id))

        signature = sign(data["pr_key"], 'LOGIN' + network_id + uid)
        pubkey = get_public_key(data["pr_key"])
        full_token = 'Bearer ' + token
        data1 = {
            'role_id': 0,
            'ecosystem': 1,
            'expire': 3600,
            'pubkey': pubkey,
            'signature': signature,
        }
        # print('actually data is {}'.format(data))
        resp = self.client.post('/login', data=data1, headers={'Authorization': full_token})
        # print("actually resp.json() is {}".format(resp.json()))

        login_token = 'Bearer ' + resp.json()['token']
        print("actually login_token is {}".format(login_token))
        tx_data = {}
        headers = {}
        # headers["User-Agent"] ='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        # headers["Connection"] = 'keep-alive'
        # headers["Content-Length"] = '100000000'
        headers["Authorization"] = login_token
        # print('get login_token url is {} and {}'.format(login_token, data["url"]))
        for i in range(1, 500):
            amount = 10*i
            redata = {"Amount": 1 * amount, "Recipient": data["Recipient"]}
            schema = api.contract(data["url"], login_token, contract_name)
            contract = Contract(schema=schema, private_key=data["pr_key"], params=redata, ecosystem_id=1)
            tx_bin_data, txhash = contract.Multiconcat()
            tx_data[txhash] = tx_bin_data
        print(tx_data)
        resp = self.client.post('/sendTx', files=tx_data, headers=headers, name=contract_name)
        print(resp.text)
        # hash = json.loads(resp.text)["hashes"]["call1"]
        # # print(hash)
        # resp_p = api.tx_status(data["url"], token, hash)
        # print("转账结果：%s" % resp_p)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://192.168.1.208:2079/api/v2"
    # host = "http://127.0.0.1:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(20):
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],

            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall50.txt', 'pr_key')[count],
            "Recipient": TestSystemContracts().catche_read('wall50.txt', 'address')[random.randint(0, 99)],
        }
        # print(data)
        queueData.put_nowait(data)


if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave3.py --slave')
    # os.system('locust -f gac_sendtokens.py')
    os.system('locust -f gac_sendtokens.py --no-web -c 1 -r 1')
