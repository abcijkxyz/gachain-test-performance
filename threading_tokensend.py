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
import json


class MyThread(threading.Thread):

    def run(self):
        """
        新用户注册登录、转账
        :return:
        """
        host = "https://node2.gachain.org:7079/api/v2"  # 链上地址
        # host = "http://127.0.0.1:7079/api/v2"     # 本地地址
        for count in range(10):
            contract_name = 'TokensSend'
            data = {
                # "url" :  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
                "no": count,
                "url": host,
                "pr_key": TestSystemContracts().catche_read('wall1000.txt', 'pr_key')[count],
                "Recipient": TestSystemContracts().catche_read('wall2000.txt', 'address')[count],
            }
            # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
            print("TokensSend no pr_key is {} and {}".format(data["no"], data["pr_key"]))
            token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
            # print("actually token is {}".format(token))

            schema = api.contract(data["url"], token, contract_name)
            redata = {'Recipient': data["Recipient"], 'Amount': '100000000'}
            contract = Contract(schema=schema, private_key=data["pr_key"], params=redata)
            tx_bin_data = contract.concat()
            resp = requests.post(data["url"] + '/sendTx', files={'call1': tx_bin_data},
                                headers={'Authorization': token})
            # print(resp.text)
            hash = json.loads(resp.text)["hashes"]["call1"]
            # print(hash)
            resp_p = api.tx_status(data["url"], token, hash)
            print("转账结果：%s" % resp_p)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


t1 = MyThread()
t1.start()
