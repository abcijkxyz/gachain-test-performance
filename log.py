# /usr/bin/python
# -*- coding:UTF-8 -*-


import sys
import os


class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(os.path.join("/logs", fileN), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
