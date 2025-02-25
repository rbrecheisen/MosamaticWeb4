import os
import numpy as np

import models

from ..task import Task
from .tensorflowmodel import TensorFlowModel
from .torchmodel import TorchModel
from ...utils import load_dicom, normalize_between, get_pixels_from_dicom_object, convert_labels_to_157
from ...managers.logmanager import LogManager

LOG = LogManager()


class MuscleFatSegmentationL3Task(Task):
    def load_model_files(self, model_dir, model_type, model_version):
        if model_type == 'torch':
            torch_model = TorchModel()
            model, contour_model, params = torch_model.load(model_dir, model_version)
            return model, contour_model, params
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            model, contour_model, params = tensorflow_model.load(model_dir, model_version)
            return model, contour_model, params
        else:
            pass
        return None

    def predict_contour(self, contour_model, img, params, model_type):
        if model_type == 'torch':
            torch_model = TorchModel()
            mask = torch_model.predict_contour(img, contour_model, params)
            return mask
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            mask = tensorflow_model.predict_contour(img, contour_model, params)
            return mask
        else:
            pass
        return None

    def process_file(self, f_path, output_dir, model, contour_model, params, model_type):
        p = load_dicom(f_path)
        if p is None:
            self.log_warning(f'File {f_path} is not valid DICOM, skipping...')
            return
        img1 = get_pixels_from_dicom_object(p, normalize=True)        
        if contour_model:
            mask = self.predict_contour(contour_model, img1, params, model_type)
            img1 = normalize_between(img1, params['min_bound'], params['max_bound'])
            img1 = img1 * mask
        img1 = img1.astype(np.float32)
        if model_type == 'torch':
            torch_model = TorchModel()
            pred_max = torch_model.predict(img1, model)
        elif model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            pred_max = tensorflow_model.predict(img1, model)
        else:
            pass
        pred_max = convert_labels_to_157(pred_max)
        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, pred_max)
        return segmentation_file_path

    def execute(self):
        # Get inputs and parameters
        input_dir = self.get_input_dir('fileset')
        model_dir = self.get_input_dir('model_fileset')
        model_type = self.get_param('model_type', 'tensorflow')
        model_version = float(self.get_param('model_version', 1.0))
        # Load models and model parameters
        model, contour_model, params = self.load_model_files(model_dir, model_type, model_version)
        if model is None or params is None:
            raise RuntimeError('Model or parameters could not be loaded')
        # Process images
        files = os.listdir(input_dir)
        nr_steps = len(files)
        output_files = []
        for step in range(nr_steps):
            if self.is_canceled():
                return None
            f = files[step]
            source = os.path.join(input_dir, f)
            # Process file and segment muscle and fat
            target = self.process_file(source, self.get_output_dir(), model, contour_model, params, model_type)
            if target is not None:
                output_files.append(target)
            self.set_progress(step, nr_steps)
        return output_files