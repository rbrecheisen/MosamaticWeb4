import os
import json
import zipfile
import numpy as np

from ...utils import normalize_between


class TensorFlowModel:
    def __init__(self):
        pass

    def load(self, model_dir, model_version):
        # Check if correct model version files exist
        for model_file_name in ['model.zip', 'contour_model.zip', 'params.json']:
            items = os.path.splitext(model_file_name)
            model_file_name_with_version = f'{items[0]}-{str(model_version)}{items[1]}'
            model_file_path_with_version = os.path.join(model_dir, model_file_name_with_version)
            if not os.path.exists(model_file_path_with_version):
                raise RuntimeError(f'Model file {model_file_path_with_version} does not exist')
        tfLoaded = False
        model, contour_model, params = None, None, None
        for f in os.listdir(model_dir):
            f_path = os.path.join(model_dir, f)
            if f == f'model-{str(model_version)}.zip':
                if not tfLoaded:
                    import tensorflow as tf # Only load TensorFlow package if necessary (takes some time)
                    tfLoaded = True
                model_dir_unzipped = os.path.join(os.path.split(f_path)[0], 'model_unzipped')
                os.makedirs(model_dir_unzipped, exist_ok=True)
                with zipfile.ZipFile(f_path) as zipObj:
                    zipObj.extractall(path=model_dir_unzipped)
                model = tf.keras.models.load_model(model_dir_unzipped, compile=False)
            elif f == f'contour_model-{str(model_version)}.zip':
                if not tfLoaded:
                    import tensorflow as tf # Only load TensorFlow package if necessary (takes some time)
                    tfLoaded = True
                contour_model_dir_unzipped = os.path.join(os.path.split(f_path)[0], 'contour_model_unzipped')
                os.makedirs(contour_model_dir_unzipped, exist_ok=True)
                with zipfile.ZipFile(f_path) as zipObj:
                    zipObj.extractall(path=contour_model_dir_unzipped)
                contour_model = tf.keras.models.load_model(contour_model_dir_unzipped, compile=False)
            elif f == f'params-{model_version}.json':
                with open(f_path, 'r') as f:
                    params = json.load(f)
            else:
                pass
        return model, contour_model, params

    def predict_contour(self, image, contour_model, params):
        ct = np.copy(image)
        ct = normalize_between(ct, params['min_bound_contour'], params['max_bound_contour'])
        img2 = np.expand_dims(ct, 0)
        img2 = np.expand_dims(img2, -1)
        pred = contour_model.predict([img2])
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=-1)
        mask = np.uint8(pred_max)
        return mask

    def predict(self, image, model):
        img2 = np.expand_dims(image, 0)
        img2 = np.expand_dims(img2, -1)
        pred = model.predict([img2])
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=-1)
        return pred_max