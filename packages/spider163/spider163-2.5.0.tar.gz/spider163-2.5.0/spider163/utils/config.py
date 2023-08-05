#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import re

PATH = os.environ.get("HOME") + "/spider163"

if os.environ.get("SPIDER163_PATH") is not None:
    PATH = os.environ.get("SPIDER163_PATH")

if not os.path.exists(PATH):
    os.makedirs(PATH)

if not os.path.exists(PATH + "/spider163.conf"):
    print("请在默认路径 " + PATH + " 下增加配置文件 spider.conf 格式参照官方")
    os._exit(-1)

cf = ConfigParser.ConfigParser()
cf.read(PATH + "/spider163.conf")


def get_path():
    return PATH


def get_db():
    return cf.get("core", "db")


def get_mysql():
    link = get_db()
    db = re.search('(?<=/)[^/]+(?=\?)', link).group(0)
    uri = re.search('.*(?=/)', link).group(0)
    return {"db": db, "uri": uri}


def get_port():
    return cf.get("core", "port")



