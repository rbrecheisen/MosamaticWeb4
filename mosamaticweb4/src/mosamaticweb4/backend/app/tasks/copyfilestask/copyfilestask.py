import os
import time
import shutil

from ..task import Task
from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    def execute(self):
        fileset = self.input_fileset('fileset')
        if fileset:
            files = fileset.files
            nr_steps = len(files)
            for step in range(nr_steps):
                if self.is_canceled():
                    return
                shutil.copy(files[step].path, os.path.join(self.output_fileset_dir, files[step].name))
                delay = self.param('delay', None)
                if delay:
                    time.sleep(int(delay))
                self.set_progress(step, nr_steps)
        else:
            raise RuntimeError('Fileset not found')