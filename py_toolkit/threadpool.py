# -*- coding: utf-8 -*-

import sys
import logging
import threading

if sys.version_info.major < 3:
    from Queue import Queue
else:
    from queue import Queue

class Worker(threading.Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks, _id, label=None):
        threading.Thread.__init__(self)
        self.name = "{1}Worker-{0}".format(_id, "{0}-".format(label) if label else "")
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                # An exception happened in this thread
                logging.exception(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()

class ThreadPool:
    """ Pool of threads consuming tasks from a queue """

    def __init__(self, num_threads, label=None):
        self.tasks = Queue(num_threads)
        for i in range(num_threads):
            Worker(self.tasks, i, label=label)

    def enqueue(self, func, *args, **kwargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kwargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.enqueue(func, args)

    def join(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()
