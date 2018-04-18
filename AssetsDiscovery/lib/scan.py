#encoding:utf-8 

import os
from datetime import date
from core.log import logger
from core.config import Config

class Scan(object):

    def __init__(self, rate=30000):
        self.target_file = Config.MSCAN_TARGET_FILE
        self.result_file = Config.MSCAN_RESULT_FILE
        self.rate = Config.MSCAN_RATE
        self.ports = Config.MSCAN_SCAN_PORTS
        self.exclude = Config.MSCAN_EXCLUDE_FILE


    def analysis(self):
        result_fp = open(self.result_file, 'r')
        result_json = result_fp.readlines()
        result_fp.close()
        del result_json[0]
        del result_json[-1]
        open_list = {}
        for res in result_json:
            try:
                # masscan can't use '.', replace with '_'
                ip = res.split()[3].replace('.', '_')
                port = res.split()[2]
                if ip in open_list:
                    open_list[ip].append(port)
                else:
                    open_list[ip] = [port]
            except Exception as ex:
                logger.exception("Analysis result error!" + ex.message)
        return open_list


    def scan(self):
        try:
            scan_text = "masscan -p {ports} -iL {target} -oL {output}  --excludefile {exclude} --randomize-hosts --rate={rate}".format( \
                        ports=self.ports, target=self.target_file, \
                        output=self.result_file, rate=self.rate, exclude=self.exclude)
            os.system(scan_text)
        except Exception, ex:
            logger.exception(ex.message)


    def run(self):
        logger.info("Masscan start by scanner...")
        self.scan()
        logger.info('Masscan done by scanner...')
        return self.analysis()