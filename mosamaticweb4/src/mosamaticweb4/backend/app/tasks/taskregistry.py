from ..tasks.copyfilestask.copyfilestask import CopyFilesTask


TASK_REGISTRY = {
    'CopyFilesTask': {
        'class': CopyFilesTask,
        'input_fileset_names': [
            'fileset',
        ],
        'output_fileset_name': 'copyfilestask',
        'params': [
            'delay',
        ],
    }
}

# from mosamaticdesktop.tasks.copyfilestask.copyfilestask import CopyFilesTask
# from mosamaticdesktop.tasks.copyfilestask.copyfilestaskdialog import CopyFilesTaskDialog
# from mosamaticdesktop.tasks.decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
# from mosamaticdesktop.tasks.decompressdicomfilestask.decompressdicomfilestaskdialog import DecompressDicomFilesTaskDialog
# from mosamaticdesktop.tasks.rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
# from mosamaticdesktop.tasks.rescaledicomfilestask.rescaledicomfilestaskdialog import RescaleDicomFilesTaskDialog
# from mosamaticdesktop.tasks.musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
# from mosamaticdesktop.tasks.musclefatsegmentationl3task.musclefatsegmentationl3taskdialog import MuscleFatSegmentationL3TaskDialog
# from mosamaticdesktop.tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
# from mosamaticdesktop.tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstaskdialog import CreatePngsFromSegmentationsTaskDialog
# from mosamaticdesktop.tasks.calculatemetricstask.calculatemetricstask import CalculateMetricsTask
# from mosamaticdesktop.tasks.calculatemetricstask.calculatemetricstaskdialog import CalculateMetricsTaskDialog


# TASK_REGISTRY = {

#     'CopyFilesTask': (
#         CopyFilesTask, 
#         CopyFilesTaskDialog, """
# CopyFilesTask
# =============
# Copies files without modification from the input directory to its output directory.

# Parameters: None
# """),

    
#     'DecompressDicomFilesTask': (
#         DecompressDicomFilesTask, 
#         DecompressDicomFilesTaskDialog, """
# DecompressDicomFilesTask
# ========================
# Loads DICOM images from the input directory and checks if they are JPEG2000 compressed. If they are, the
# DICOM files will be decompressed and saved to the output directory. If not, they will be copied without
# modification to the output directory.

# Parameters: None
# """),

    
#     'RescaleDicomFilesTask': (
#         RescaleDicomFilesTask, 
#         RescaleDicomFilesTaskDialog, """
# RescaleDicomFilesTask
# =====================
# Rescales DICOM files to 512 x 512 if needed. If files are rescaled 
# their file names will be written to an output file 'rescaled_files.txt' 
# and the rescaled files will be saved in the output directory. If no rescaling
# is needed, they will be copied without modification to the output directory.

# Parameters:
#  - Target image size: Number of pixels in both rows and columns of the image.
# """),

    
#     'MuscleFatSegmentationL3Task': (
#         MuscleFatSegmentationL3Task, 
#         MuscleFatSegmentationL3TaskDialog, """
# MuscleFatSegmentationL3Task
# =========================
# Runs automatic segmentation of muscle and fat on the L3 images. Requires
# loading the AI model files in the task parameters dialog. 

# Parameters:
#  - Model directory: Directory containing PyTorch model files.
# """),

    
#     'CreatePngsFromSegmentationsTask': (
#         CreatePngsFromSegmentationsTask, 
#         CreatePngsFromSegmentationsTaskDialog, """
# CreatePngsFromSegmentationTask
# ==============================
# Creates PNG images of segmentation files created by MuscleFatSegmentationL3Task. 

# Parameters:
#  - Figure width: Width of the figure (default: 10).
#  - Figure height: Height of the figure (default: 10).
# """),

    
#     'CalculateMetricsTask': (
#         CalculateMetricsTask, 
#         CalculateMetricsTaskDialog, """
# CalculateMetricsTask
# ====================
# Calculate a number of body composition metrics from the muscle and fat regions
# segmented by the MuscleFatSegmentationL3Task. Requires loading of the original 
# DICOM images as well, probably the output images of the DecompressDicomFilesTask or
# RescaleDicomFilesTask. These images can be loaded in the task parameters dialog.

# Parameters: 
#  - Image directory: Directory containing original images (possibly rescaled).
#  - Patient heights: CSV file containing patient heights.
# """),
# }