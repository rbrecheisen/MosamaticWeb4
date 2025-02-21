# import os
# import time
# import json
# import shutil

# from pathlib import Path
# from enum import Enum


# class TaskStatus(Enum):
#     IDLE = 'idle'
#     RUNNING = 'running'
#     CANCELED = 'canceled'
#     FAILED = 'failed'
#     COMPLETED = 'completed'


# class Task:
#     def __init__(self, input_dir, output_dir_name=None, params=None):
#         super(Task, self).__init__()
#         self._input_dir = input_dir
#         if output_dir_name is None:
#             output_dir_name = self.__class__.__name__.lower()
#         self._output_dir = os.path.join(str(Path(self._input_dir).parent), output_dir_name)
#         self._params = params
#         self._canceled = False
#         clean_output = self.get_param('clean_output', False)
#         if clean_output and os.path.exists(self._output_dir):
#             self.log_info(f'Deleting output directory for task {self.__class__.__name__}...')
#             shutil.rmtree(self._output_dir)
#         os.makedirs(self._output_dir, exist_ok=False)

#     def get_input_dir(self):
#         return self._input_dir
    
#     def get_output_dir(self):
#         return self._output_dir
    
#     def has_param(self, name):
#         if self._params is not None:
#             return name in self._params.keys()
#         return False
    
#     def get_params(self):
#         return self._params
    
#     def get_param(self, name, default=None):
#         if self.has_param(name):
#             return self._params[name]
#         return default
    
#     def is_canceled(self):
#         return self._canceled

#     def execute(self):
#         for i in range(5):
#             if self._canceled:
#                 self.set_status(TaskStatus.CANCELED)
#                 return 
#             time.sleep(1)
#             self.set_progress(i, 5)

#     def run(self):
#         self.set_status(TaskStatus.RUNNING)
#         try:
#             self.log_info(f'Input directory: {self.get_input_dir()}')
#             self.log_info(f'Output directory: {self.get_output_dir()}')
#             self.log_info('Parameters:')
#             self.log_info(json.dumps(self.get_params(), indent=2))
#             self.execute()
#             if not self.is_canceled():
#                 self.set_status(TaskStatus.COMPLETED)
#         except Exception as e:
#             self.log_error(f'ERROR: Task failed ({e})')
#             self.set_status(TaskStatus.FAILED)

#     def cancel(self):
#         self._canceled = True

#     def log_info(self, message):
#         message = f'[INFO] {message}'

#     def log_warning(self, message):
#         message = f'[WARNING] {message}'

#     def log_error(self, message):
#         message = f'[ERROR] {message}'

#     def set_progress(self, step, nr_steps):
#         progress = int(((step + 1) / (nr_steps)) * 100)
#         self.log_info(f'Progress task {self.__class__.__name__}: {progress}')

#     def set_status(self, status, message=None):
#         if not message:
#             message = ''
#         self.log_info(f'Status task {self.__class__.__name__}: {status.value} ({message})')
