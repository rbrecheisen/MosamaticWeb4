import os
import time
import shutil

from ..task import Task
from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    def execute(self):
        input_dir = self.get_input_dir('fileset')
        output_dir = self.get_output_dir()
        os.makedirs(output_dir, exist_ok=True)
        files = os.listdir(input_dir)
        nr_steps = len(files)
        for step in range(nr_steps):
            if self.is_canceled():
                return
            source = os.path.join(input_dir, files[step])
            target = os.path.join(output_dir, files[step])
            shutil.copy(source, target)
            LOG.info(f'Copied {source} to {target}')
            delay = self.get_param('delay', None)
            if delay:
                time.sleep(int(delay))
            self.set_progress(step, nr_steps)