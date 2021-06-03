# /usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------------------------------
# Name: 20190122001.py
# Author: Sect.Leuce
# Email: 812570241@qq.com
# Created: 2019/1/22 13:41
# Desc:
# ------------------------------------------------------------------------------------------------


import os
import time
import json
import random
import linecache
import queue
from libs import actions, tools, db, contract, check, api
from genesis_blockchain_tools.contract import Contract
from genesis_blockchain_tools.crypto import genesis, gen_keypair
# from genesis_blockchain_tools.convert import genesis
import xlrd
import binascii


class TestSystemContracts(object):
    def __init__(self, nodename=None):
        self.nodename = nodename
        if self.nodename == 'node':
            config = tools.read_config('nodes')
            self.url = config[0]['url']
            self.db = config[0]['db']
            self.wait = tools.read_config('test')['wait_tx_status']
            self.pr_key = config[0]['private_key']
            data = actions.login(self.url, self.pr_key, 0)
            self.token = data['jwtToken']

            # self.keys = tools.read_fixtures('keys')
        else:
            pass

    def callMulti(self, name, data, sleep):
        resp = actions.call_multi_contract(self.url, self.pr_key, name, data, self.token)
        print("resp", resp)
        time.sleep(sleep)
        if 'hashes' in resp:
            result = actions.tx_status_multi(self.url, self.wait, resp['hashes'], self.token)
            # for status in result.values():
            #     self.unit.assertNotIn('errmsg', status)
            #     self.unit.assertGreater(int(status['blockid']), 0, 'BlockID not generated')

    # 导入合约
    def import_tt(self, apps=None):
        for app_name in apps:
            print("import---->", app_name)
            path = os.path.join(os.getcwd(), 'apps', app_name)
            tx = contract.import_upload(self.url, self.pr_key, self.token, path)
            tx0 = check.is_tx_in_block(self.url, self.wait, tx, self.token)
            founder_id = actions.get_parameter_value(self.url, 'founder_account', self.token)
            import_app_data = db.get_import_app_data(self.db, founder_id)
            import_app_data = import_app_data['data']
            contract_name = 'Import'
            data = [{'contract': contract_name,
                     'params': import_app_data[i]} for i in range(len(import_app_data))]
            self.callMulti(contract_name, data, 10)
            time.sleep(1)

    # 登录gachain
    def login_gachain(self, filename):
        f = open(filename)
        addrfile = open("addr.txt", 'a', encoding='utf-8')
        for line in f.readlines():
            pr_key = line.strip('\n')
            data = actions.login(self.url, pr_key, 0)
            print("data", data)
            addr = data['address']
            addrfile.writelines('\n'+addr)
            time.sleep(1)
        f.close()
        addrfile.close()

    # 去除文件中的空行
    def read_line(self, filename1, filename2):
        file1 = open(filename1, 'r', encoding='utf-8')  # 要去掉空行的文件
        file2 = open(filename2, 'w', encoding='utf-8')
        try:
            for line in file1.readlines():
                if line.split():
                    file2.writelines(line)
        finally:
            file1.close()
            file2.close()

    # 发送初始资金
    def token_send(self, filename):
        f = open(filename)
        contract_name = 'TokensSend'
        for line in f.readlines():
            data = {'Recipient': line, 'Amount': '1000000'}
            schema = api.contract(self.url, self.token, contract_name)
            contract = Contract(schema=schema, private_key=self.pr_key,
                                params=data)
            tx_bin_data = contract.concat()
            print("resp ", api.send_tx(self.url, self.token, {'call1': tx_bin_data}))

    # 创建生态系统
    def creat_ecosystem(self, filename):
        f = open(filename)
        ecofile = open("eco.txt", 'a', encoding='utf-8')
        eco_no = api.ecosystems(self.url, self.token)['number'] + 1
        for line in f.readlines():

            self.pr_key = line.strip('\n')
            data = actions.login(self.url, self.pr_key, 0)
            self.token = data['jwtToken']
            # self.token = "".join(tuple(api.getuid(self.url)))
            contract.new_ecosystem(self.url,self.pr_key,self.token,"eco"+str(eco_no))
            ecofile.writelines('\n' + self.pr_key)
            eco_no = eco_no+1

    # 删除已经使用的钱包数据
    def remove_file(self, filename):
        dirPath = "E:/python_project/apla-tests_20181218/test_tools/"
        print('移除前test目录下有文件：%s' % os.listdir(dirPath))
        # 判断文件是否存在
        for i in range(len(filename)):
            if (os.path.exists(dirPath + filename[i])):
                os.remove(dirPath + filename[i])
                print('移除后test 目录下有文件：%s' % os.listdir(dirPath))
            else:
                print("要删除的文件不存在！")

    # 生成用户
    def create_user(self, wall_filename, user_num):
        users = {}
        addrfile = open(wall_filename, 'a', encoding='utf-8')
        for i in range(user_num):
            priv_key, pub_key = gen_keypair()
            print(priv_key, pub_key)
            users["pr_key"] = priv_key
            pub_key_hex = bytes().fromhex(pub_key)
            users["address"] = genesis.public_key_to_address(pub_key_hex)
            print(json.dumps(users))
            addrfile.writelines(json.dumps(users)+'\n')

    def create_user1(self, wall_filename, user_num):
        users = {}
        addrfile = open(wall_filename, 'a', encoding='utf-8')
        for i in range(user_num):
            time.sleep(1)
            tx = contract.new_user(self.url, self.pr_key, self.token)
            time.sleep(1)
            data = actions.login(self.url, tx["pr_key"], 0)
            time.sleep(3)
            print("data", data["jwtToken"])
            # contract.tokens_send(self.url, self.pr_key, self.token, data["address"], '100000000000000')
            users["pr_key"] = tx["pr_key"]
            users["jwtToken"] = data["jwtToken"]
            print("users", json.dumps(users))
            addrfile.writelines(json.dumps(users) + '\n')

    # 缓存读取
    def catche_read(self, path, key):
        if os.path.exists(path):
            content = []
            cache_data = linecache.getlines(path)
            for line in range(len(cache_data)):
                if line == 0:
                    pass
                elif key == "pr_key":
                    content.append(eval(cache_data[line].lstrip('\n'))["pr_key"])
                elif key == "token":
                    content.append(eval(cache_data[line].lstrip('\n'))["token"])
                else:
                    content.append(eval(cache_data[line].lstrip('\n'))["address"])

                # content = json.loads(content)

                # content = ast.literal_eval(content)
            return content
        else:
            print('the path [{}] is not exist!'.format(path))

    # 缓存读取矿机地址、矿机编号、激活私钥、激活公钥
    def catche_read_xlsx(self, path):
        if os.path.exists(path):
            content = []
            book = xlrd.open_workbook(os.path.join(os.getcwd(), path))
            sheet = book.sheet_by_index(0)
            data_dict = {}
            data_dict['data'] = []
            # 临时头
            tmp_titles = sheet.row_values(0)
            # 文件内容总行数
            nrows = sheet.nrows
            # 去空格后的头部
            titles = []
            for v in tmp_titles:
                v = "{}".format(v)
                titles.append(v.strip())
            # 头部信息
            if 'title' not in data_dict.keys():
                data_dict['title'] = titles
                # 对数据进行处理，返回字典
                for line in range(1, nrows):
                    line_dict = dict(zip(titles, sheet.row_values(line)))
                    data_dict['data'].append(line_dict)
            return data_dict['data']
        else:
            print('the path [{}] is not exist!'.format(path))

    def search_ecosys(self):
        api.ecosystems(self.url, self.token)


if __name__ == "__main__":
    # 删除测试用历史数据
    # TestSystemContracts().remove_file(["addr.txt", "addr_1.txt", "node_prikey_1.txt", "subnode_prikey_1.txt", "eco.txt"])
    # # 导入合约
    # TestSystemContracts("node").import_tt(['1_system.json', '2_conditions.json', '3_basic.json', '4_lang_res.json', '6_ecosystems_catalog.json'])
    # # 读取主节点私钥
    # TestSystemContracts().read_line("node_prikey.txt", "node_prikey_1.txt")
    # # 读取子节点私钥
    # TestSystemContracts().read_line("subnode_prikey.txt", "subnode_prikey_1.txt")
    # TestSystemContracts("node").login_gachain("node_prikey_1.txt")
    # TestSystemContracts("node").login_gachain("subnode_prikey_1.txt")
    # TestSystemContracts().read_line("addr.txt", "addr_1.txt")
    # TestSystemContracts("node").token_send("addr_1.txt")
    # TestSystemContracts("node").creat_ecosystem("subnode_prikey_1.txt")
    # TestSystemContracts("node").search_ecosys()
    # TestSystemContracts("node").create_user("user100000.txt", 100000)
    # TestSystemContracts("node").create_user("wall1000.txt", 1000)
    # TestSystemContracts("node").create_user("user1.txt", 1000)
    rep = TestSystemContracts().catche_read('wall1000.txt', 'address')[random.randint(0, 5)]
    print(rep)
    # TestSystemContracts("node").create_user("wall2500.txt", 2500)
    # TestSystemContracts("node").create_user("wall3000.txt", 3000)
    # TestSystemContracts("node").create_user("wall4000.txt", 4000)
    # TestSystemContracts("node").create_user("wall5000.txt", 5000)
    # TestSystemContracts("node").create_user1("token10.txt", 10)
    # bind_obj = TestSystemContracts("node")
    # rep = bind_obj.catche_read_xlsx('minedata/Mine_Batch_info_214.xlsx')[random.randint(0, 1)]
    # data = {
    #
    #     "mine_active_pri_key": rep.get("Activate the private key"),
    #     "mine_active_pub_key": rep.get("Activate the public key"),
    # }
    # print(data)
    # print(TestSystemContracts("node").catche_read('wall1-1.txt', 'pr_key')[random.randint(0, 10)])
    # print(TestSystemContracts().catche_read('wall5000.txt', 'address')[random.randint(0, 10)])
