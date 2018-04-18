# -*- coding:utf-8 -*-
import logging
def log(name=None):
    logger = logging.getLogger(__name__)
    if not name:
        name=__name__
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(name)

    logging.basicConfig(format='%(name)s:%(asctime)s %(filename)s %(process)d[%(funcName)s line:%(lineno)d] %(levelname)s:%(message)s',level=logging.DEBUG,datafmt='%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler(name+'.log','a')
    #fh = logging.FileHandler('log.log','a')
    formatter = logging.Formatter('%(name)s:%(asctime)s %(filename)s %(process)d[%(funcName)s line:%(lineno)d] %(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger

def get_log(name=None):
    #logger = logging.getLogger(__name__+'.log')
    if not name:
        name=__name__
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(name)
    logging.basicConfig(format='%(name)s:%(asctime)s %(filename)s %(process)d[%(funcName)s line:%(lineno)d] %(levelname)s:%(message)s',level=logging.DEBUG,datafmt='%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler('log_main_control.log','a')
    formatter = logging.Formatter('%(name)s:%(asctime)s %(filename)s %(process)d[%(funcName)s line:%(lineno)d] %(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger
    #return logging.getLogger(__name__+'.log')

if __name__ == '__main__':
    logger = log()
    logger.debug('debug')
