#encoding:utf-8

import os
from log import logger
import threading
from thread import error as threadError
import time
import sys


def runThreads(numThreads, threadFunction, threadArgs, startThreadMsg=True):
    """
    args
    numThreads: the number of threads
    threadFunction: handler function of threads
    threadArgs: arguments for handler function
    startThreadMsg: message for starting thread
    """

    threads = []
    try:
        if numThreads > 1:
            if startThreadMsg:
                infoMsg = "starting %d threads" % numThreads
                logger.info(infoMsg)
        else:
            threadFunction()
            return

        for numThread in xrange(numThreads):
            try:
                thread = threading.Thread(target=threadFunction, name=str(numThread), args=[threadArgs])
            except Exception as ex:
                errmsg = '%s occurred error: %s' % (threading.currentThread().getName(), err)
                logger.exception(ermsg)   
                sys.exit(1)

            setDaemon(thread)

            try:
                thread.start()
            except threadError, errMsg:
                errMsg = "error occurred while starting new thread ('%s')" % errMsg
                logger.exception(errMsg)
                break
            threads.append(thread)
        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

    except KeyboardInterrupt:
        if numThreads > 1:
            logger.info("waiting for threads to finish (Ctrl+C was pressed)")
        try:
            while(threading.activeCount() > 1):
                pass
        except KeyboardInterrupt:
            raise Exception('user aborted (Ctrl+C was pressed multiple times')

    except Exception as e:
        errmsg = 'thread %s: %s ' % (threading.currentThread().getName(), e.message)
        logger.exception(errmsg)


def setDaemon(thread):
    thread.daemon = True

        