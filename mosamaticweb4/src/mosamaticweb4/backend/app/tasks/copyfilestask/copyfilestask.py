import time
from ..task import Task

from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    def run(self):
        for i in range(5):
            LOG.info(f'Iteration {i}')
            delay = self.param('delay', None)
            if delay:
                time.sleep(int(delay))