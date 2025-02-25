import os
import numpy as np

from ..task import Task
from ...utils import convert_numpy_array_to_png_image, AlbertaColorMap


class CreatePngsFromSegmentationsTask(Task):
    def execute(self):
        input_dir = self.get_input_dir('segmentation_fileset')
        files = os.listdir(input_dir)
        nr_steps = len(files)
        output_files = []
        for step in range(nr_steps):
            if self.is_canceled():
                return 
            # Convert source image to PNG format and copy to output
            f = files[step]
            source = os.path.join(input_dir, f)
            source_image = np.load(source)
            png_file_name = os.path.split(source)[1] + '.png'
            png_file_path = convert_numpy_array_to_png_image(
                source_image, 
                self.get_output_dir(), 
                AlbertaColorMap(), 
                png_file_name,
                fig_width=self.get_param('fig_width', 10),
                fig_height=self.get_param('fig_height', 10),
            )
            # Update progress
            self.set_progress(step, nr_steps)
            output_files.append(png_file_path)
        return output_files