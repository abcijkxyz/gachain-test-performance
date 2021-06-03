# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave7.py
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


class WebsiteTasks(TaskSet):

    @task
    def v_mine_incomehistory(self):
        """
        查询接口——v_mine_incomehistory
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
        print('actually resp.json() is {}'.format(resp.json()))
        login_token = 'Bearer ' + resp.json()['token']
        keyid = resp.json()['key_id']
        res = self.client.post('/listWhere/v_mine_incomehistory?limit=10&offset=0&order=id desc&where={"keyid":"' + keyid +'"}',
                               headers={'Authorization': login_token})
        print('actually no result is {} and {}'.format(data["no"], res.json()))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://node2.gachain.org:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    for count in range(1):
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall4000.txt', 'pr_key')[count],
        }
        queueData.put_nowait(data)

if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave7.py --slave')
    os.system('locust -f gac_locust_run_slave7.py --no-web -c 1 -r 1')
