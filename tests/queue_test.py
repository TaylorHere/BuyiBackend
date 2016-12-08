# coding:utf-8
from redis import Redis
from rq import Queue
import sys
q = Queue(connection=Redis())
from develop_test import main
if __name__ == '__main__':
    local = sys.argv[1]
    loop = int(sys.argv[2])
    counter = 0
    for i in xrange(loop):
    	q.enqueue(main,local,1)
    	counter = counter +1
    	print counter