# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: threading_login.py
# Author: lahaer
# Email: 1607787244@qq.com
# Created: 2020/3/2 14:57
# Desc:
# ------------------------------------------------------------------------------------------------

from libs import actions, tools, api
from pftest001 import TestSystemContracts
import threading
import time
import random
import json

class MyThread(threading.Thread):

    def run(self):
        """
        登录新建用户并保存token
        :return:
        """
        host = "http://3.1.66.88:7079/api/v2"  # 链上地址
        # host = "http://127.0.0.1:7079/api/v2"     # 本地地址
        for count in range(600, 3000):
            users = {}
            addrfile = open('token10.txt', 'a', encoding='utf-8')
            data = {
                "no": count,
                "url": host,
                "pr_key": TestSystemContracts().catche_read('wall4000.txt', 'pr_key')[count],
            }
            # print('actually url pr_key is {} and {}'.format(data['url'], data['pr_key']))
            print("actually no pr_key is {} and {}".format(data["no"], data["pr_key"]))
            token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
            print("token is {}".format(token))
            users["pr_key"] = data["pr_key"]
            users["token"] = token
            print("users", json.dumps(users))
            addrfile.writelines(json.dumps(users) + '\n')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

t1 = MyThread()
t1.start()
