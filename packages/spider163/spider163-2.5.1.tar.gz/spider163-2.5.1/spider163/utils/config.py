#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import ConfigParser


PATH = os.environ.get("HOME") + "/spider163"
if os.environ.get("SPIDER163_PATH") is not None:
    PATH = os.environ.get("SPIDER163_PATH")

if not os.path.exists(PATH):
    os.makedirs(PATH)
cf = ConfigParser.ConfigParser()
if not os.path.exists(PATH + "/spider163.conf"):
    print("请在默认路径 " + PATH + " 下增加配置文件 spider163.conf 格式参照官方")
    cf.read("data/spider163.conf")
else:
    cf.read(PATH + "/spider163.conf")


def get_path():
    return PATH


def get_db():
    try:
        return cf.get("core", "db")
    except Exception as e:
        print("配置文件存在问题，请在 {}/spider163.conf 中配置db=xxx选项".format(PATH))
        print("错误详情： {}".format(e))
        raise e


def get_mysql():
    link = get_db()
    db = re.search('(?<=/)[^/]+(?=\?)', link).group(0)
    uri = re.search('.*(?=/)', link).group(0)
    return {"db": db, "uri": uri}


def get_port():
    try:
        return cf.get("core", "port")
    except Exception as e:
        print("配置文件存在问题，请在 {}/spider163.conf 中配置port=xxx选项".format(PATH))
        print("错误详情： {}".format(e))
        raise e




