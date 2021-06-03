# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave9.py
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
    def monthehistorydetial(self):
        """
        查询接口——monthehistorydetial
        :return:
        """
        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            # print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)

        print('actually url pr_key is {} and {}'.format(data['url'], data['pr_key']))

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
        # print('actually resp.json() is {}'.format(resp.json()))
        login_token = 'Bearer ' + resp.json()['token']
        keyid = resp.json()['key_id']

        # login_token1 = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlY29zeXN0ZW1faWQiOiIxIiwia2V5X2lkIjoiLTc1NjI3NzE5OTYxOTI1MDI2MDgiLCJhY2NvdW50X2lkIjoiMTA4OC0zOTcyLTA3NzUtMTcwNC05MDA4Iiwicm9sZV9pZCI6IjAiLCJleHAiOjE1ODMyNTMwNTl9.L2-sMQdn1v7rl3yhtg6JpxD-JcttQNbxaVumBm_khPs"
        # keyid1 = "-7562771996192502608"

        redata = {"ecosystem": 1, "order": "id desc", "page": 0, "limit": 5, "zone": -8, "time": 1582992000,
                  "keyid": keyid}
        redata = json.dumps(redata)
        res = self.client.post('/monthehistorydetial', data=redata,
                               headers={'Authorization': login_token})
        # print('actually res.json() is {}'.format(res.json()))
        message = res.json()["message"]
        if message == "Success":
            print('actually no result is {} and {}'.format(data["no"], "Success"))
        else:
            print('actually no result is {} and {}'.format(data["no"], "Failure"))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://mineapi.gachain.org:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(10):
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall2500.txt', 'pr_key')[count],
        }
        queueData.put_nowait(data)

if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave9.py --slave')
    os.system('locust -f gac_locust_run_slave9.py --no-web -c 1 -r 1')
