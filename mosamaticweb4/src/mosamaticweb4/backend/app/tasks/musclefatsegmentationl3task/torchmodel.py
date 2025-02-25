import os
import json
import torch
import cv2
import numpy as np

from models import UNet
from torch.nn import MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d

from ...utils import normalize_between


class TorchModel:
    def __init__(self):
        pass

    def load(self, model_dir, model_version):
        # Check if correct model version files exist
        for model_file_name in ['model.pth', 'contour_model.pth', 'params.json']:
            items = os.path.splitext(model_file_name)
            model_file_name_with_version = f'{items[0]}-{str(model_version)}{items[1]}'
            model_file_path_with_version = os.path.join(model_dir, model_file_name_with_version)
            if not os.path.exists(model_file_path_with_version):
                raise RuntimeError(f'Model file {model_file_path_with_version} does not exist')
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            f_path = os.path.join(model_dir, f)
            with torch.serialization.safe_globals([UNet, MaxPool2d, Sequential, Conv2d, PReLU, BatchNorm2d, Dropout, ConvTranspose2d]):
                if f == f'model-{str(model_version)}.pth':
                    model = torch.load(f_path, map_location=torch.device('cpu'))
                    model.to('cpu')
                    model.eval()
                elif f == f'contour_model-{str(model_version)}.pth':
                    contour_model = torch.load(f_path, map_location=torch.device('cpu'))
                    contour_model.to('cpu')
                    contour_model.eval()
                elif f == f'params-{str(model_version)}.json':
                    with open(f_path, 'r') as obj:
                        params = json.load(obj)
                else:
                    pass
        return model, contour_model, params

    def predict_contour(self, image, contour_model, params):
        ct = np.copy(image)
        ct = normalize_between(ct, params['min_bound_contour'], params['max_bound_contour'])
        target_shape = (512, 512)  
        ct_resized = cv2.resize(ct, target_shape, interpolation=cv2.INTER_LINEAR)
        ct_resized_tensor = torch.tensor(ct_resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to('cpu')
        with torch.no_grad():
            pred = contour_model(ct_resized_tensor).cpu().numpy()
        pred_max = pred.argmax(axis=1)
        mask = np.uint8(pred_max)
        return mask

    def predict(self, image, model):
        img1_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0).to('cpu')
        with torch.no_grad():
            pred = model(img1_tensor).cpu().numpy()
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=0)
        return pred_max