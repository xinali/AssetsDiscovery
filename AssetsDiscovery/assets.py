#encoding:utf-8

import os
import sys
from datetime import date, timedelta

from lib.core.log import logger
from lib.core.config import Config
from lib.scan import Scan
from lib.core.db import mongo
from lib.utils.sendmail import send_mail
from lib.findassets import AssetsCompare

def insert_data(insert_time, open_ip_ports):
    try:
        data = {
            'time': insert_time,
            'data': open_ip_ports
        }
        if not mongo[Config.MONGO_C_MASSCAN].find_one({"time":insert_time}):
            mongo[Config.MONGO_C_MASSCAN].insert_one(data)
    except Exception as ex:
        logger.error(ex.message)


def send_message(email_address='1447932441@qq.com', email_data='test email'):
# def send_message(email_address='xuweiwei01@shandagames.com', email_data='test email'):
    subject = u'资产发现系统 by 安全实验室' 
    to_list = email_address
    content = email_data
    send_mail(subject, to_list, content)


def find():

    # client = MongoDB() 
    # print client.db
    # client.collection.drop()
    try:
        scan_obj = Scan() 
        open_ip_ports = scan_obj.run()
        for ip, port in open_ip_ports.items():
            print ip, port
        # open_ip_ports = {'192_168_1_1': [89, 99, 89]}
        insert_time = str(date.today())
        insert_data(insert_time, open_ip_ports)
        logger.info('Insert data successfully in ' + insert_time)
    except Exception as ex:
        logger.exception(ex.message)

    try:
        assets = AssetsCompare()
        not_in_enq, not_in_all = assets.find_assets()
        if not_in_enq:
            mail_content = u'发现不在设备管理平台设备,如下：\r\n'
            mail_content += '\r\n'.join([ ip.replace('_', '.') for ip in not_in_enq ])
            send_message(email_data=mail_content)

        if not_in_all:
            mail_content = u'发现新增幽灵设备,如下：\r\n'
            mail_content += '\r\n'.join([ ip.replace('_', '.') for ip in not_in_all ])
            send_message(email_data=mail_content)
        
        logger.info('Send message successfully...')
    except Exception as ex:
        logger.exception(ex.message)
        sys.exit(1)
