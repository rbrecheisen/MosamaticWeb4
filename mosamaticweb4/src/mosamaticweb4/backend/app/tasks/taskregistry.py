from ..tasks.copyfilestask.copyfilestask import CopyFilesTask
from ..tasks.decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from ..tasks.rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from ..tasks.musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
from ..tasks.calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from ..tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask


TASK_REGISTRY = {
    'CopyFilesTask': {
        'class': CopyFilesTask,
        'description': 'Copies files to new fileset without modification',
        'input_fileset_names': [
            'fileset',
        ],
        'output_fileset_name': 'copyfilestask',
        'params': [
            'delay',
        ],
    },
    'DecompressDicomFilesTask': {
        'class': DecompressDicomFilesTask,
        'description': 'Decompresses DICOM files (if necessary)',
        'input_fileset_names': [
            'fileset',
        ],
        'output_fileset_name': 'decompressdicomfilestask',
        'params': None,
    },
    'RescaleDicomFilesTask': {
        'class': RescaleDicomFilesTask,
        'description': 'Rescales DICOM files (if necessary) to a square target size (default: 512)',
        'input_fileset_names': [
            'fileset',
        ],
        'output_fileset_name': 'rescaledicomfilestask',
        'params': [
            'target_size',
        ],
    },
    'MuscleFatSegmentationL3Task': {
        'class': MuscleFatSegmentationL3Task,
        'description': 'Runs muscle and fat segmentation at L3',
        'input_fileset_names': [
            'fileset',
            'model_fileset',
        ],
        'output_fileset_name': 'musclefatsegmentationl3task',
        'params': [
            'model_type',
            'model_version',
        ],
    },
    'CalculateMetricsTask': {
        'class': CalculateMetricsTask,
        'description': 'Calculate body composition metrics',
        'input_fileset_names': [
            'fileset',
            'segmentation_fileset',
        ],
        'output_fileset_name': 'calculatemetricstask',
        'params': None,
    },
    'CreatePngsFromSegmentationsTask': {
        'class': CreatePngsFromSegmentationsTask,
        'description': 'Creates PNG images of segmentation masks',
        'input_fileset_names': [
            'segmentation_fileset',
        ],
        'output_fileset_name': 'createpngsfromsegmentationstask',
        'params': None,
    },
}