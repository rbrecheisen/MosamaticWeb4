import time
from ..task import Task, TaskStatus

from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    def execute(self):
        for i in range(5):
            if self.is_canceled():
                # self.set_status(TaskStatus.CANCELED)
                return
            delay = self.param('delay', None)
            if delay:
                time.sleep(int(delay))
            self.set_progress(i, 5)