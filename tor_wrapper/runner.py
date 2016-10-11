# coding: utf8
"""


"""
import multiprocessing
import signal
import sys
import traceback

import os

from tor_wrapper import onions_scan

__author__ = 'clement.trebuchet@gmail.com'

FLAG_CLEAR = b'0'

workers = []


def die_handler(signum, frame):
    for proc_list in workers:
        for proc in proc_list:
            try:
                proc.terminate()
            except Exception as e:
                print('[//] {}'.format(e))


class AutomateManager(object):
    """This is the runner class for Behave automate
       This run tests in parallel (as many processes as set in the configuration file)

    Attributes
    ----------
        jobs: list
            the jobs dicts list to proceed
        procs_num: int
            the number of  processes to use
        workers: list()
            the list for holding jobs
        workers_in: list()
            the list for holding input Queues()
        workers_out: Queue()
            the output queue to hold results of the computation of jobs across processes

    Methods
    -------
        wait_results
            Yields stout and stderr of the behave execution

    """

    def __init__(self, configuration, jobs=None):
        """Initialize  manager class

        Parameters
        ----------
        configuration; configObj()

        jobs: list()
            list of dicts
                {'__func__': function.__signature___,
                'params': {
                'ios_configuration': 'value',
                 ...
                 }
                }

        """
        signal.signal(signal.SIGINT, die_handler)
        signal.signal(signal.SIGTERM, die_handler)
        if jobs is None:
            raise ValueError('jobs cannot be None')
        elif not isinstance(jobs, list):
            raise TypeError('jobs must be a list of dicts')

        self.jobs = jobs
        try:
            self.procs_num = int(configuration['procs_num'])
            self._prepare()
            self._create_ipc()
            self._start()
            self._populate()

        except Exception as e:
            print(e)
            traceback.print_exc()

    def _prepare(self):
        """create appropriate handlers

        Returns
        -------

        """
        self.workers = []
        self.workers_in = []
        self.workers_out = multiprocessing.Queue()

    def _create_ipc(self):
        """prepare processes in accordance with wanted processes number in the configuration
           first putting a Queue in the workers_in list, and holding is place for reference
           second create a process with the Queue for input, the Queue for output and the process reference

           This will act as an IPC, sharing parameters and data across separate process


        """
        print(self.workers_in)
        for proc in range(self.procs_num):
            self.workers_in.append(multiprocessing.Queue())
            kwargs = {'in': self.workers_in[proc], 'oq': self.workers_out, 'id': proc}
            self.workers.append(multiprocessing.Process(target=worker, kwargs=kwargs))

        workers.append(self.workers)

    def _start(self):
        """Start processes"""
        try:

            [self.workers[proc].start() for proc in range(self.procs_num)]

        except Exception as e:
            print(e)

    def _populate(self):
        """populate queue with data for the worker (dispatching data among number of created processes)
           when filling the queue is done, put the FLAG_CLEAR at the end of each queue
           Meaning a pipe like this:
                    Queue1 > data_to_proceed, data_to_proceed, FLAG_CLEAR



        """
        for index, job in enumerate(self.jobs):
            dispatch = int(index % self.procs_num)  # this modulo operation will dispatch jobs along processes
            self.workers_in[dispatch].put(
                {
                    '__func__': job['__func__'],
                    'params': job['params']
                }
            )

        [self.workers_in[proc].put(FLAG_CLEAR) for proc in range(self.procs_num)]  # put the FLAG

    def wait_results(self):
        """This methods yield result of the computation of processes

        Yields
        ------
        tuple
            stdout, stderr, exit_code

        """
        flags = []
        while 1:
            result = self.workers_out.get()
            if isinstance(result, tuple):
                print('Receive clear flag for process {}'.format(result[0]))
                flags.append(result)
                if len(flags) == self.procs_num:
                    break
            else:
                yield result


def worker_stopped_handler(signum, frame):
    print('[**] stop worker {}'.format(frame))
    for wl in workers:
        for p in wl:
            p.terminate()


def worker(**data):
    """Stop if FLAG_CLEAR
       Execute callback function passed in kwargs

    Parameters
    ----------
    data: dict
        inq: Queue() in
        oq: Queue() out
        id: int() identifier

    """

    signal.signal(signal.SIGINT, worker_stopped_handler)
    signal.signal(signal.SIGTERM, worker_stopped_handler)
    import time
    counter = 0
    while True:
        counter += 1
        to_proceed = data.get('in').get()

        if to_proceed == FLAG_CLEAR:
            try:
                data.get('in').task_done()
            except ValueError:
                pass
            data.get('oq').put((data.get('id'), FLAG_CLEAR))
            return
        result = to_proceed.get('__func__')(**to_proceed.get('params'))
        data.get('oq').put(result)
        time.sleep(0.01)


if __name__ == '__main__':
    if os.path.exists("onion_master_list.txt"):

        with open("onion_master_list.txt", "rb") as fd:

            stored_onions = fd.read().splitlines()
        jobs = []
        for onion in stored_onions:
            jobs.append({'__func__': onions_scan.scan,
                         'params': {'url_list': [onion]}
                         })
        auto = AutomateManager({'procs_num': 3}, jobs=jobs)

    else:
        print("[!] No onion master list. Download it!")
        sys.exit(0)
