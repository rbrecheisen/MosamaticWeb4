import os
import time
import shutil

from ..task import Task


class CopyFilesTask(Task):
    def execute(self):
        input_dir = self.get_input_dir('fileset')
        files = os.listdir(input_dir)
        nr_steps = len(files)
        output_files = []
        for step in range(nr_steps):
            if self.is_canceled():
                return None
            f = files[step]
            source = os.path.join(input_dir, f)
            target = os.path.join(self.get_output_dir(), f)
            shutil.copy(source, target)
            output_files.append(target)
            delay = self.get_param('delay', None)
            if delay:
                time.sleep(int(delay))
            self.set_progress(step, nr_steps)
        return output_files