import os
import time
import shutil

from ..task import Task
from ...managers.logmanager import LogManager

LOG = LogManager()


class CopyFilesTask(Task):
    
    def execute(self):

        # Get single input directory
        input_dir = self.get_input_dir('fileset')

        # Get output directory and create it if needed
        output_dir = self.get_output_dir()
        os.makedirs(output_dir, exist_ok=True)

        # List files in input directory
        files = os.listdir(input_dir)

        # List for output files
        output_files = []

        # Determine number of steps needed for this task so
        # we can update progress correctly
        nr_steps = len(files)

        # Run through the files
        for step in range(nr_steps):

            # Check if task has been canceled and return if so
            if self.is_canceled():
                return
            
            # Build source and target file paths
            source = os.path.join(input_dir, files[step])
            target = os.path.join(output_dir, files[step])

            # Copy source file to target file
            shutil.copy(source, target)

            # Append target file to list of output files
            output_files.append(target)

            # Check if a delay was specified in the task parameters
            # and if so wait a while
            delay = self.get_param('delay', None)
            if delay:
                time.sleep(int(delay))

            # Update task progress
            self.set_progress(step, nr_steps)

        # Return list of output files
        return output_files