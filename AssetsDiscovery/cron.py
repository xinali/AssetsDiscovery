#encoding:utf-8 

import sys
import schedule                                                                                                              
import time                                                                                                                  
import os                                                                                                                    
from lib.core.log import logger
from assets import find
import psutil
                                                                                                                             
def job():                                                                                                                   
    logger.info('Checking masscan by cron job...')
    try:
        sign = False
        for process_name in psutil.process_iter(attrs=['name']):
            if 'masscan' in process_name.name():
                sign = True
                break
        # masscan is not running, then run
        if not sign:
            find()
        else:
            logger.info('Masscan is running by cron job...')
        logger.info('Check masscan done by cron job...')
    except Exception as ex:
        logger.exception(ex.message)
                                                                                                                             

def run():                                                                                                                  
    try:
        schedule.every().day.at("22:00").do(job)
        # for first run
        sign = False
        for process_name in psutil.process_iter(attrs=['name']):
            if 'masscan' in process_name.name():
                sign = True

        if not sign:
            find()
                                                                                                                                
        while True:                                                                                                              
            schedule.run_pending()                                                                                               
            time.sleep(25)                                                                                                        
    except Exception as ex: 
        logger.exception(ex.message)
        sys.exit(1)
            
                                                                                                                             
if __name__ == "__main__":                                                                                                   
    logger.info("Start AssetsDiscovery...")
    run()