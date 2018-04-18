#encoding:utf-8 

from pymongo import MongoClient
import pymysql 

from config import Config
from log import logger

try:
    client = MongoClient(host=Config.MONGO_HOST, \
                                port=Config.MONGO_PORT)
    mongo = client[Config.MONGO_DB]
except Exception as ex:
    logger.exception(ex.message)

try:
    mysql = pymysql.connect(host=Config.MYSQL_HOST,
                            port=Config.MYSQL_PORT,
                            user=Config.MYSQL_USER,
                            password=Config.MYSQL_PASSWORD,
                            db=Config.MYSQL_DB,
                            cursorclass=pymysql.cursors.DictCursor)

except Exception as ex:
    logger.exception(ex)
