import concurrent.futures
import queue
import threading
from concurrent.futures import wait
from typing import Optional, List

from src.locale import locale
from src.log.logger import logger

_ = locale.lc


class DetectTask:

    def __init__(self, index, id, len, p, func) -> None:
        super().__init__()
        self.p = p
        self.index = index
        self.id = id
        self.len = len
        self.func = func


class DetectExecutor:
    lock = threading.Lock()

    def __init__(self, max, batch) -> None:
        super().__init__()
        self.max = max
        self.batch = batch
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max)
        self.task_queue = queue.Queue()
        self.futures: Optional[List[concurrent.futures.Future]] = []
        self.results = {}
        self.index = 0

    def add_task(self, task):
        self.task_queue.put(task)

    def run(self):
        if self.task_queue.empty():
            return
        total = self.task_queue.qsize()
        for i in range(self.batch):
            self.futures.append(self.executor.submit(self._process_tasks, total))

    def _process_tasks(self, total):
        while not self.task_queue.empty():
            try:
                task: Optional[DetectTask] = self.task_queue.get()
                logger.debug(f'process_task: start task_id = {task.id} thread = {threading.currentThread().name}')
                result = task.func(task.id, task.p)
                text_info = _("Progress: %s, %s detect %s, score %.2f, cost %.2fs%s")
                self.results[task.id] = result
                with self.lock:
                    logger.info(f'{text_info}',
                                f'{self.index + 1}/{total}',
                                result.filename,
                                result.tag,
                                round(result.score, 2) if result.score else 0,
                                result.cost,
                                f'{", excluded" if result.exclude else ""}')
                    self.index = self.index + 1
            except Exception as e:
                logger.exception(e)

    def wait_completion(self):
        wait(self.futures)
        results = self.get_results()
        self.reset()
        return results

    def get_results(self):
        return self.results

    def reset(self):
        self.results = {}
        self.index = 0

    def stop(self):
        self.executor.shutdown()


def init_executor():
    return DetectExecutor(3, 3)
