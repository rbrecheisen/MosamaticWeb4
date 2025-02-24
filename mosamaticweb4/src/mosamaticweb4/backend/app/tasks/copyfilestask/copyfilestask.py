import time
from ..task import Task

from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    def execute(self):
        fileset = self.input_fileset('fileset')
        if fileset:
            nr_steps = fileset.size
            for step in range(nr_steps):
                if self.is_canceled():
                    return
                delay = self.param('delay', None)
                if delay:
                    time.sleep(int(delay))
                self.set_progress(step, nr_steps)
        else:
            raise RuntimeError('Fileset not found')