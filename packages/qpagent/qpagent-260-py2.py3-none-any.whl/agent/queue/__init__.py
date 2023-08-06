#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import logging
from threading import Lock
from threading import Thread

from agent.consts import AgentWorkerType
from agent.worker.android_monkey import AndroidMonkey
from agent.worker.appcrawler import Appcrawler
from agent.worker.compatibility import Compatibility
from agent.worker.ios_monkey import iosmonkey
from agent.worker.macaca import Macaca
from agent.worker.xiaomi import XiaomiCrawler
from agent.worker.appstore import AppStoreCrawler

logger = logging.getLogger(__name__)

monkey_mutex = Lock()
appcrawler_mutex = Lock()


class TaskQueue(Queue.Queue):
    def __init__(self, num_workers=1):
        Queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.start_workers()

    def add_task(self, worker_type, data):
        self.put((worker_type, data))

    def start_workers(self):
        for i in range(self.num_workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            worker_type, data = self.get(True)
            if worker_type is AgentWorkerType.androidmonkey.value:
                logger.info('android monkey-------task id:' + str(data))
                monkey_mutex.acquire()
                AndroidMonkey(data).run()
                monkey_mutex.release()
            elif worker_type is AgentWorkerType.selenium.value:
                logger.info('selenium-------task id:' + str(data))
                Compatibility(data).run()
            elif worker_type is AgentWorkerType.appcrawler.value:
                logger.info('app crawler-------task id:' + str(data))
                appcrawler_mutex.acquire()
                Appcrawler(data).run()
                appcrawler_mutex.release()
            elif worker_type is AgentWorkerType.macaca.value:
                logger.info('macaca-------task id:' + str(data))
                Macaca(data).run()
            elif worker_type is AgentWorkerType.iosmonkey.value:
                logger.info('ios monkey-------task id:' + str(data))
                iosmonkey(data).run()
            elif worker_type is AgentWorkerType.crawler.value:
                logger.info('crawler-------task id:' + str(data.get('task_id')))
                crawler_type = data.get('crawler_type')
                if crawler_type == 'appstore':
                    AppStoreCrawler(data).crawl()
                elif crawler_type == 'xiaomi':
                    XiaomiCrawler(data).crawl()
