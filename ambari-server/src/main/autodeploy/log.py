#!/usr/bin/python
#coding=utf-8


# logging.basicConfig(level=logging.DEBUG,
#   format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#   datefmt='[%m-%d %H:%M:%S]',
#   filename='/tmp/deploy.log',
#   filemode='a')
# 
# logger = logging.getLogger('tbds.deploy')


import logging

# 创建一个logger
logger = logging.getLogger('deploy')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('deploy.log', encoding = "utf-8")
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

