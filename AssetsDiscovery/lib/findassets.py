#encoding:utf-8 

from datetime import date, timedelta

from core.db import mysql, mongo
from core.config import Config
from core.log import logger
from IPython import embed

import traceback
import sys

class AssetsCompare(object):
    def __init__(self):
        self.cursor = mysql.cursor()
        self.all_enq_ips = [] # all enquipment platform ips
        self.not_in_enq = []
        self.not_in_all = []

        self.das_ips = [] # for reserved
        self.firewall_ips = [] # for reserved
        self.storage_ips = [] # for reserved
        self.switch_ips = [] # for reserved

    def sql_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def get_company_assets(self):
        try:
            # get DAS_SVR_Info ip
            das = [] # [[out1, out2, in1, in2], ]
            das_ips = [] # [ip, ip, ip]
            query_das = 'select OuterIP1, OuterIP2, InnerIP1, InnerIP2 from DAS_SVR_Info'
            result = self.sql_query(query_das)
            for server in result:
                single_server = []
                for des, ip in server.items():
                    if ip:
                        single_server.append(ip)
                        das_ips.append(ip)
                if single_server:
                    das.append(single_server)
            
            if das_ips:
                self.all_enq_ips += das_ips
        except Exception as ex:
            logger.exception('Get DAS_SVR_Info Error:' + ex.message)

        try:
            # get SP_Firewall_Info Ip
            query_firewall = 'select Ip from SP_Firewall_Info'
            result = self.sql_query(query_firewall)
            # embed()
            firewall = [ ip['Ip'] for ip in result if ip['Ip'] ]
            if firewall:
                self.all_enq_ips += firewall
        except Exception as ex:
            logger.exception('Get SP_Firewall_Info Error:' + ex.message)

        try:
            # get SP_Storage_Info MainIP
            query_storage = 'select MainIP from SP_Storage_Info'
            result = self.sql_query(query_storage)
            if result:
                storage = [ ip['MainIP'] for ip in result if ip['MainIP'] ]
                if storage:
                    self.all_enq_ips += storage
        except Exception as ex:
            logger.exception('Get SP_Storage_Info Error:' + ex.message)

        try:
            # get SP_Switch_Info Ip 
            query_switch = 'select Ip from SP_Switch_Info'
            result = self.sql_query(query_switch)
            if result:
                switch = [ ip['Ip'] for ip in result if ip['Ip'] ]
                if switch:
                    self.all_enq_ips += switch
        except Exception as ex:
            logger.exception('Get SP_Switch_Info Error:' + ex.message)

        # save all equipment platform ips to masscan exclude
        fp = open('data/masscan/exclute.txt', 'w')
        unique_ips = set(self.all_enq_ips)
        for ip in unique_ips:
            fp.write(ip + '\n')
        fp.close()

        return set(unique_ips)


    def find_assets(self):
        # NewAssets = []

        today_data = None
        yesterday_data = None

        try:
            today = date.today()
            today_str = str(today)     
            # today_str = '2018-03-14'
            tmp_data = mongo[Config.MONGO_C_MASSCAN].find_one({'time':today_str})
            if tmp_data:
                today_data = tmp_data['data']
        except Exception as ex:
            logger.exception("Get today data error!" + ex.message)
            sys.exit(1)

        try:
            yesterday = today - timedelta(1)
            yesterday_str = str(yesterday) # yyy-mm-dd
            tmp_data = mongo[Config.MONGO_C_MASSCAN].find_one({'time':yesterday_str})
            if tmp_data:
                yesterday_data = tmp_data['data']
        except Exception as ex:
            logger.exception("Get yestoday data error " + ex.message)
            sys.exit(1)

        # first compare with enquipment ips then yesterday data
        self.get_company_assets()
        try:
            for ip in today_data:
                if ip not in self.all_enq_ips:
                    self.not_in_enq.append(ip)
                    if not yesterday_data:
                        continue
                    elif ip not in yesterday_data.keys():
                        self.not_in_all.append(ip)
        except Exception as ex:
            logger.exception("Compare Error!" + ex.message)
            sys.exit(1)
        
        return self.not_in_enq, self.not_in_all