#coding=utf-8
import time
import Queue
from threading import Thread


msg_queue = Queue.Queue(maxsize=10)


class Job(object):
    def __init__(self, name):
        self.name = name
        print 'name:%s\n' % name
        return


def put_msg(queue):
    while True:
        if queue.qsize() < 5:
            for i in xrange(5):
                queue.put(Job(i))
                queue.task_done()
        else:
            time.sleep(1)

worker = Thread(target=put_msg, args=(msg_queue,))
worker.setDaemon(True)
worker.start()


while True:
    next_job = msg_queue.get()
    print 'Processing job:%s\n' % next_job.name