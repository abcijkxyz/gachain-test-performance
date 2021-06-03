# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: gac_locust_run_slave1.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/2/24 14:57
# Desc:
# ------------------------------------------------------------------------------------------------
import datetime
import random
from locust import HttpLocust, TaskSet, task, between
from libs import actions, api
from pftest001 import TestSystemContracts
from genesis_blockchain_tools.crypto import sign
from genesis_blockchain_tools.crypto import get_public_key
import queue
import os
import time
import sys
from log import Logger


class WebsiteTasks(TaskSet, Logger):

    # def on_start(self):
    #     sys.stdout = Logger('tests.log')  # 控制台输出日志

    @task
    def register_login(self):
        """
        新用户注册登录
        :return:
        """
        try:
            data = self.locust.queueData.get()
            self.locust.queueData.put_nowait(data)
            print(data)
        except queue.Empty:
            print('no data exist')
            exit(0)
        # print('actually url pr_key Recipient is {} and {}'.format(data['url'], data['pr_key'],data['Recipient']))
        print("actually slave1 pr_key is {}".format(data["pr_key"]))
        print("actually start time is {}".format(time.time()))

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
        print("actually end time is {}".format(time.time()))
        print("actually resp.json() is {}".format(resp.json()))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # sys.stdout = Logger('tests.log')  # 控制台输出日志


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://127.0.0.1:7079/api/v2"
    queueData = queue.Queue()  # 队列实例化
    wait_time = between(2, 5)
    # tasks = [WebsiteTasks]
    for count in range(50):
        data = {
            # "url":  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],

            "no": count,
            "url": host,
            "pr_key": TestSystemContracts().catche_read('wall50.txt', 'pr_key')[count],
        }
        queueData.put_nowait(data)

    print(queueData)


if __name__ == "__main__":
    # os.system('locust -f gac_locust_run_slave1.py --slave')
    # 有web界面测试
    os.system('locust -f gac_locust_run_slave1.py')
    # 无web界面测试
    # os.system('locust -f gac_locust_run_slave1.py --no-web -c 2000 -r 2000')
    # 负载测试
    # os.system('locust -f gac_locust_run_slave1.py --no-web -c 100 -r 10 --run-time=300 --step-load --step-clients 10 --step-time 30')
    # os.system('locust -f gac_locust_run_slave1.py  --step-load')

