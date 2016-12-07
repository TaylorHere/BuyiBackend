# coding=utf-8
import sys
import os
import multiprocessing
import gevent.monkey
gevent.monkey.patch_all()

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)

worker_class = 'gunicorn.workers.ggevent.GeventWorker'
workers = multiprocessing.cpu_count() * 2 + 1

chdir = path_of_current_dir
log_dir = '/var/escort'
worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'debug'

reload = True
debug = True

bind = "%s:%s" % ("0.0.0.0", 8081)
pidfile = '%s/log/%s.pid' % (log_dir, _file_name)
logfile = '%s/log/%s.pid' % (log_dir, _file_name)
#errorlog = '%s/log/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/log/%s_access.log' % (log_dir, _file_name)
