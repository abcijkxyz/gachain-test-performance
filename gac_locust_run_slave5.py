# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave5.py
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
import json
from genesis_blockchain_tools.crypto import sign
from genesis_blockchain_tools.crypto import get_public_key


class WebsiteTasks(TaskSet):

    @task
    def mine_pledge(self):
        """
        激活矿机、质押矿机
        :return:
        """
        contract_name1 = 'ActiveMineInfo'
        contract_name2 = 'NewMineStake'
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
        print('actually dev_addr is {} '.format(data['dev_addr']))

        # 用户登录
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
        resp = self.client.post('/login', data=data1, headers={'Authorization': full_token})
        login_token = 'Bearer ' + resp.json()['token']

        # 用户激活矿机
        signature = sign(data["mine_active_pri_key"], "123")
        redata1 = {'DevActivePubKey': data["mine_active_pub_key"], 'Sign': signature, 'Data': "123",
                  'Invite': ""}
        # print("redata1", redata1)
        schema = api.contract(data["url"], login_token, contract_name1)
        contract = Contract(schema=schema, private_key=data["pr_key"], params=redata1, ecosystem_id=1)
        tx_bin_data = contract.concat()
        # print("tx_bin_data", tx_bin_data)
        rep1 = self.client.post('/sendTx', files={'call1': tx_bin_data}, headers={'Authorization': login_token},
                                name=contract_name1)
        # print(rep1.text)
        hash1 = json.loads(rep1.text)["hashes"]["call1"]
        # print(hash1)
        resp_p1 = api.tx_status(data["url"], token, hash1)
        print("用户激活矿机结果：%s" % resp_p1)

        # 用户质押矿机
        schema = api.contract(data["url"],  login_token, contract_name2)
        redata2 = {'DevAddr': data["dev_addr"], "Cycle": 10, "Amount": 10000}
        contract = Contract(schema=schema, private_key=data["pr_key"], params=redata2, ecosystem_id=1)
        tx_bin_data = contract.concat()
        # print("tx_bin_data", tx_bin_data)
        rep2 = self.client.post('/sendTx', files={'call1': tx_bin_data}, headers={'Authorization': login_token},
                                name=contract_name2)
        # print(rep2.text)
        hash2 = json.loads(rep2.text)["hashes"]["call1"]
        # print(hash2)
        resp_p2 = api.tx_status(data["url"], token, hash2)
        print("用户质押矿机结果：%s" % resp_p2)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://node2.gachain.org:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(10):
        mine_info = TestSystemContracts().catche_read_xlsx('mine_info1.xlsx')[random.randint(101, 300)]
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],

            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall4000.txt', 'pr_key')[count],  # 不同的人多次质押
            "mine_active_pri_key": mine_info.get("Activate the private key"),
            "mine_active_pub_key": mine_info.get("Activate the public key"),
            "dev_addr": mine_info.get("Miner address")
        }
        queueData.put_nowait(data)

if __name__ == "__main__":
    os.system('locust -f gac_locust_run_slave5.py --slave')
    # os.system('locust -f gac_locust_run_slave5.py --no-web -c 100 -r 10')
