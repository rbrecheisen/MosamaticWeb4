import os
import time
import warnings
import math
import pendulum
import pydicom
import numpy as np

from PIL import Image
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian

warnings.filterwarnings("ignore", message="Invalid value for VR UI:", category=UserWarning)


def create_name_with_timestamp(prefix: str='') -> str:
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S%f')[:17]
    if prefix != '' and not prefix.endswith('-'):
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name


def current_time_in_milliseconds() -> int:
    return int(round(time.time() * 1000))


def current_time_in_seconds() -> int:
    return int(round(current_time_in_milliseconds() / 1000.0))


def elapsed_time_in_milliseconds(start_time_in_milliseconds: int) -> int:
    return current_time_in_milliseconds() - start_time_in_milliseconds


def elapsed_time_in_seconds(start_time_in_seconds: int) -> int:
    return current_time_in_seconds() - start_time_in_seconds


def duration(seconds: int) -> str:
    h = int(math.floor(seconds/3600.0))
    remainder = seconds - h * 3600
    m = int(math.floor(remainder/60.0))
    remainder = remainder - m * 60
    s = int(math.floor(remainder))
    return '{} hours, {} minutes, {} seconds'.format(h, m, s)


def is_dicom(f: str) -> bool:
    try:
        pydicom.dcmread(f, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False
    

def load_dicom(f):
    if is_dicom(f):
        return pydicom.dcmread(f)
    return None


def is_jpeg2000_compressed(p: pydicom.FileDataset):
    return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]


def get_pixels_from_dicom_object(p: pydicom.FileDataset, normalize: bool=True) -> np.array:
    pixels = p.pixel_array
    if not normalize:
        return pixels
    if normalize is True: # Map pixel values back to original HU values
        return p.RescaleSlope * pixels + p.RescaleIntercept
    if isinstance(normalize, int):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize
    if isinstance(normalize, list):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize[1] + normalize[0]
    return pixels


def convert_labels_to_157(label_image: np.array) -> np.array:
    label_image157 = np.copy(label_image)
    label_image157[label_image157 == 1] = 1
    label_image157[label_image157 == 2] = 5
    label_image157[label_image157 == 3] = 7
    return label_image157


def normalize_between(img: np.array, min_bound: int, max_bound: int) -> np.array:
    img = (img - min_bound) / (max_bound - min_bound)
    img[img > 1] = 0
    img[img < 0] = 0
    c = (img - np.min(img))
    d = (np.max(img) - np.min(img))
    img = np.divide(c, d, np.zeros_like(c), where=d != 0)
    return img


def apply_window_center_and_width(image: np.array, center: int, width: int) -> np.array:
    image_min = center - width // 2
    image_max = center + width // 2
    windowed_image = np.clip(image, image_min, image_max)
    windowed_image = ((windowed_image - image_min) / (image_max - image_min)) * 255.0
    return windowed_image.astype(np.uint8)


def calculate_area(labels: np.array, label, pixel_spacing) -> float:
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixel_spacing[0] * pixel_spacing[1]) / 100.0
    return area


def calculate_index(area: float, height: float) -> float:
    return area / (height * height)


def calculate_mean_radiation_attenuation(image: np.array, labels: np.array, label: int) -> float:
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    mask_sum = np.sum(mask)
    if mask_sum > 0.0:
        mean_radiation_attenuation = np.sum(subtracted) / np.sum(mask)
    else:
        # print('Sum of mask pixels is zero, return zero radiation attenuation')
        mean_radiation_attenuation = 0.0
    return mean_radiation_attenuation


def calculate_dice_score(ground_truth: np.array, prediction: np.array, label: int) -> float:
    numerator = prediction[ground_truth == label]
    numerator[numerator != label] = 0
    n = ground_truth[prediction == label]
    n[n != label] = 0
    if np.sum(numerator) != np.sum(n):
        raise RuntimeError('Mismatch in Dice score calculation!')
    denominator = (np.sum(prediction[prediction == label]) + np.sum(ground_truth[ground_truth == label]))
    dice_score = np.sum(numerator) * 2.0 / denominator
    return dice_score


def convert_dicom_to_numpy_array(dicom_file_path: str, window_level: int=50, window_width: int=400, normalize=True) -> np.array:
    p = pydicom.dcmread(dicom_file_path)
    pixels = p.pixel_array
    pixels = pixels.reshape(p.Rows, p.Columns)
    if normalize:
        b = p.RescaleIntercept
        m = p.RescaleSlope
        pixels = m * pixels + b
    pixels = apply_window_center_and_width(pixels, window_level, window_width)
    return pixels


class ColorMap:
    def __init__(self, name: str) -> None:
        self._name = name
        self._values = []

    def name(self) -> str:
        return self._name
    
    def values(self):
        return self._values
    

class GrayScaleColorMap(ColorMap):
    def __init__(self) -> None:
        super(GrayScaleColorMap, self).__init__(name='GrayScaleColorMap')
        # Implement your own gray scale map or let NumPy do this more efficiently?
        pass    

class AlbertaColorMap(ColorMap):
    def __init__(self) -> None:
        super(AlbertaColorMap, self).__init__(name='AlbertaColorMap')
        for i in range(256):
            if i == 1:  # muscle
                self.values().append([255, 0, 0])
            elif i == 2:  # inter-muscular adipose tissue
                self.values().append([0, 255, 0])
            elif i == 5:  # visceral adipose tissue
                self.values().append([255, 255, 0])
            elif i == 7:  # subcutaneous adipose tissue
                self.values().append([0, 255, 255])
            elif i == 12:  # unknown
                self.values().append([0, 0, 255])
            else:
                self.values().append([0, 0, 0])


def apply_color_map(pixels: np.array, color_map: ColorMap) -> np.array:
    pixels_new = np.zeros((*pixels.shape, 3), dtype=np.uint8)
    np.take(color_map.values(), pixels, axis=0, out=pixels_new)
    return pixels_new


def convert_numpy_array_to_png_image(
        numpy_array_file_path_or_object: str, output_dir_path: str, color_map: ColorMap=None, png_file_name: str=None, fig_width: int=10, fig_height: int=10) -> str:
    if isinstance(numpy_array_file_path_or_object, str):
        numpy_array = np.load(numpy_array_file_path_or_object)
    else:
        numpy_array = numpy_array_file_path_or_object
        if not png_file_name:
            raise RuntimeError('PNG file name required for NumPy array object')
    if color_map:
        numpy_array = apply_color_map(pixels=numpy_array, color_map=color_map)
    image = Image.fromarray(numpy_array)
    if not png_file_name:
        numpy_array_file_name = os.path.split(numpy_array_file_path_or_object)[1]
        png_file_name = numpy_array_file_name + '.png'      
    elif not png_file_name.endswith('.png'):
        png_file_name += '.png'
    png_file_path = os.path.join(output_dir_path, png_file_name)
    image.save(png_file_path)
    return png_file_path

