# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: threading_tokenssend.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/3/2 14:57
# Desc:
# ------------------------------------------------------------------------------------------------
from libs import actions, tools, api
from genesis_blockchain_tools.contract import Contract
from pftest001 import TestSystemContracts
import threading
import time
import requests
import random
from genesis_blockchain_tools.crypto import sign
import json


class MyThread(threading.Thread):

    def run(self):
        """
        新用户注册登录、激活矿机
        :return:
        """
        host = "https://node21.gachain.org:7079/api/v2"  # 链上地址
        # host = "http://127.0.0.1:7079/api/v2"     # 本地地址
        for count in range(20):
            contract_name = 'ActiveMineInfo'
            mine_info = TestSystemContracts().catche_read_xlsx('Mine_info(zhen).xlsx')[count]
            data = {
                # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
                "no": count,
                "url": host,
                # "pr_key": TestSystemContracts().catche_read('wall2500.txt', 'pr_key')[count],
                "pr_key": "55bde7b83e62271fa978b572b4c7a1bddb7b449ddb2b8cbf023224e811bdf284",
                "mine_active_pri_key": mine_info.get("Activate the private key"),
                "mine_active_pub_key": mine_info.get("Activate the public key"),
            }
            # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
            print("actually no pr_key is {} and {}".format(data["no"], data["pr_key"]))
            print('actually mine_active_pri_key is {} '.format(data['mine_active_pri_key']))
            print('actually mine_active_pub_key is {} '.format(data['mine_active_pub_key']))

            token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
            # print("actually token is {}".format(token))
            signature = sign(data["mine_active_pri_key"], "123")
            redata = {'DevActivePubKey': data["mine_active_pub_key"], 'Sign': signature, 'Data': "123",
                      'Invite': ""}

            schema = api.contract(data["url"], token, contract_name)
            contract = Contract(schema=schema, private_key=data["pr_key"], params=redata)
            tx_bin_data = contract.concat()
            resp = requests.post(data["url"] + '/sendTx', files={'call1': tx_bin_data},
                                 headers={'Authorization': token})

            # print(resp.text)
            hash = json.loads(resp.text)["hashes"]["call1"]
            # print(hash)
            resp_p = api.tx_status(data["url"], token, hash)
            print(resp_p)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


t1 = MyThread()
t1.start()
