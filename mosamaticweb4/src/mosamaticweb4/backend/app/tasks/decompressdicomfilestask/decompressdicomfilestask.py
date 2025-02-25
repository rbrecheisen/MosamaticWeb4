import os
import shutil

from ..task import Task
from ...managers.logmanager import LogManager
from ...utils import is_jpeg2000_compressed, is_dicom, load_dicom

LOG = LogManager()


class DecompressDicomFilesTask(Task):
    def execute(self):
        # Get input files
        input_dir = self.get_input_dir('fileset')
        files = os.listdir(input_dir)
        nr_steps = len(files)
        output_files = []
        # Process only DICOM files
        for step in range(nr_steps):
            if self.is_canceled():
                return None
            f = files[step]
            source = os.path.join(input_dir, f)
            if is_dicom(source):
                target = os.path.join(self.get_output_dir(), f)
                p = load_dicom(source)
                if is_jpeg2000_compressed(p):
                    p.decompress()
                    p.save_as(target)
                else:
                    shutil.copy(source, target)
                output_files.append(target)
            # Update progress
            self.set_progress(step, nr_steps)
        return output_files