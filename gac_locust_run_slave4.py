# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave4.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/24 14:57
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
from genesis_blockchain_tools.crypto import sign
from genesis_blockchain_tools.crypto import get_public_key
import json


class WebsiteTasks(TaskSet):

    @task
    def active_mine(self):
        """
        激活矿机
        :return:
        """
        contract_name = 'ActiveMineInfo'
        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            # print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)

        print('actually url pr_key is {} and {}'.format(data['url'], data['pr_key']))
        print('actually mine_active_pri_key is {} '.format(data['mine_active_pri_key']))
        print('actually mine_active_pub_key is {} '.format(data['mine_active_pub_key']))

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

        signature = sign(data["mine_active_pri_key"], "123")
        redata = {'DevActivePubKey': data["mine_active_pub_key"], 'Sign': signature, 'Data': "123",
                  'Invite': ""}
        print("redata", redata)
        schema = api.contract(data["url"],  login_token, contract_name)
        contract = Contract(schema=schema, private_key=data["pr_key"], params=redata, ecosystem_id=1)
        tx_bin_data = contract.concat()
        # print("tx_bin_data", tx_bin_data)
        resp = self.client.post('/sendTx', files={'call1': tx_bin_data}, headers={'Authorization': login_token},
                                name=contract_name)
        # print(resp.text)
        hash = json.loads(resp.text)["hashes"]["call1"]
        # print(hash)
        resp_p = api.tx_status(data["url"], token, hash)
        print("用户激活矿机结果：%s" % resp_p)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://node1.gachain.org:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(2):
        # print('actually count is {} '.format(count))
        mine_info = TestSystemContracts().catche_read_xlsx('mine_info1.xlsx')[random.randint(100, 200)]
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall2500.txt', 'pr_key')[count],
            "mine_active_pri_key": mine_info.get("Activate the private key"),
            "mine_active_pub_key": mine_info.get("Activate the public key"),
        }
        print(mine_info)
        queueData.put_nowait(data)

if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave4.py --slave')
    os.system('locust -f gac_locust_run_slave4.py --no-web -c 1 -r 1')
