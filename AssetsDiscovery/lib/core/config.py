#encoding:utf-8 

from datetime import date
import os

class MongoConfig(object): 
    # HOST = '127.0.0.1' 
    MONGO_HOST = '172.18.9.3' 
    MONGO_PORT = 27017
    MONGO_DB = 'Assets'
    MONGO_C_MASSCAN = "MScan"
    MONGO_DB_USER = 'assets'
    MONGO_DB_PASSWORD = 'assets####'


class MysqlConfig(MongoConfig):
    MYSQL_HOST = '119.97.160.240'
    MYSQL_PORT = 3306
    MYSQL_DB = 'Fscan'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'hzr1937'


class MScanConfig(MysqlConfig):
    MSCAN_RATE = 40000
    MSCAN_SCAN_PORTS = '1-65535'
    MSCAN_TARGET_FILE = 'data/masscan/target.txt'
    MSCAN_EXCLUDE_FILE = 'data/masscan/exclude.txt'
    MSCAN_RESULT_FILE = 'data/masscan/result/' + str(date.today()) + '.txt'
    # True: store data to mongodb 
    MSCAN_STORE_DATA = True


class Config(MScanConfig):   
    if os.path.isdir('/logs'):
        LOG_FILE = '/logs/assets.log'
    else:
        LOG_FILE = './assets.log'