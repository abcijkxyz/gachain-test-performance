# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: init_pool.py
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
import json
import random
from genesis_blockchain_tools.crypto import sign


class MyThread(threading.Thread):

    def run(self):
        """
        创建初始化矿池
        :return:
        """
        host = "https://node21.gachain.org:5079/api/v2"  # 链上地址
        # host = "http://127.0.0.1:7079/api/v2"     # 本地地址
        for count in range(20):
            contract_name1 = 'NewPoolRequest'
            contract_name2 = 'PoolRequestDecision'
            pool_info = TestSystemContracts().catche_read_xlsx('init_pool.xlsx')[count]
            data = {
                # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
                "no": count,
                "url": host,
                "pr_key": pool_info.get("Owner_pri_key"),
                "Name": pool_info.get("Name"),
                "SettleType": pool_info.get("SettleType"),
                "SettleRate": pool_info.get("SettleRate"),
                "SettleMinAmount": pool_info.get("SettleMinAmount"),
                "SettleCycle": pool_info.get("SettleCycle"),
                "PoolAddr": pool_info.get("PoolAddr")
            }
            # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
            print("actually no pr_key is {} and {}".format(data["no"], data["pr_key"]))
            print('actually Name SettleType SettleRate SettleMinAmount SettleCycle PoolAddr is {} and {} and {} and {} and {} and {}'
                  .format(data['Name'], data['SettleType'], data['SettleRate'], data['SettleMinAmount'],
                          data['SettleCycle'], data['PoolAddr']))
            token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
            # print("actually token is {}".format(token))
            redata1 = {"Logo": 1, "Name": data['Name'], "SettleType": data['SettleType'],
                       "SettleRate": data['SettleRate'], "SettleMinAmount": data['SettleMinAmount'],
                       "SettleCycle": data['SettleCycle'], "WebUrl": "https://www.baidu.com",
                       "PoolAddr": data['PoolAddr']}
            schema = api.contract(data["url"], token, contract_name1)
            contract = Contract(schema=schema, private_key=data["pr_key"], params=redata1)
            tx_bin_data = contract.concat()
            rep1 = requests.post(data["url"] + '/sendTx', files={'call1': tx_bin_data},
                                 headers={'Authorization': token})
            # print(rep1.text)
            hash1 = json.loads(rep1.text)["hashes"]["call1"]
            # print(hash1)
            resp_p1 = api.tx_status(data["url"], token, hash1)
            print("申请矿池结果：%s" % resp_p1)

            # 审核矿池
            manager_private_key = "55bde7b83e62271fa978b572b4c7a1bddb7b449ddb2b8cbf023224e811bdf284"
            token1 = actions.login(data["url"], manager_private_key, 12)['jwtToken']
            redata2 = {"PRId": count + 1, "Opt": "accept"}
            schema = api.contract(data["url"], token1, contract_name2)
            contract = Contract(schema=schema, private_key=manager_private_key, params=redata2)
            tx_bin_data = contract.concat()
            rep2 = requests.post(data["url"] + '/sendTx', files={'call1': tx_bin_data},
                                 headers={'Authorization': token1})
            # print(rep2.text)
            hash2 = json.loads(rep2.text)["hashes"]["call1"]
            # print(hash2)
            resp_p2 = api.tx_status(data["url"], token1, hash2)
            print("审核结果：%s" % resp_p2)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


t1 = MyThread()
t1.start()
