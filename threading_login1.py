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


class MyThread(threading.Thread):

    def run(self):
        """
        新用户注册登录
        :return:
        """
        host = "http://3.1.66.88:7079/api/v2"  # 链上地址
        # host = "http://127.0.0.1:7079/api/v2"     # 本地地址
        for count in range(0, 499):
            data = {
                # "url" :  ["http://47.106.120.16:7079/api/v2", "http://47.106.120.16:7079/api/v2"][random.randint(0, 1)],
                "no": count,
                "url": host,
                "pr_key": TestSystemContracts().catche_read('wall500.txt', 'pr_key')[count],
            }
            # print('actually url pr_key is {} and {}'.format(data['url'], data['pr_key']))
            print("actually no pr_key is {} and {}".format(data["no"], data["pr_key"]))
            token = actions.login(data["url"], data["pr_key"], 0)['jwtToken']
            print("token is {}".format(token))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

t1 = MyThread()
t1.start()
