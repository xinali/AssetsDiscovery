#encoding:utf-8 

import sys
import os 
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../")


from lib.core.db import mongo
from lib.core.threads import runThreads
from lib.core.config import Config
from poc import run
from Queue import Queue


def main():
    thread_nums = 50
    port = None # vul port
    result = mongo[Config.MONGO_C_MASSCAN].find({'port':port}, {'ip':1, 'port':1, '_id':0})
    ip_ports = Queue()

    for data in result:
        ip = data['ip']
        port = data['port']
        if not type(port) == str:
            port = str(port)
        ip_ports.put(ip + ':' + port)
    
    runThreads(thread_nums, run, ip_ports)

if __name__ == '__main__':
    main()