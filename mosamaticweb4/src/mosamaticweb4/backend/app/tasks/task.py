class Task:
    def __init__(self, input_filesets, params):
        self._input_filesets = input_filesets
        self._params = params

    def input_filesets(self):
        return self._input_filesets

    def has_param(self, name):
        if self._params is not None:
            return name in self._params.keys()
        return False
    
    def param(self, name, default=None):
        if self.has_param(name):
            return self._params[name]
        return default
    
    def run(self):
        raise NotImplementedError()

# import time

# from enum import Enum


# class TaskStatus(Enum):
#     IDLE = 'idle'
#     RUNNING = 'running'
#     CANCELED = 'canceled'
#     FAILED = 'failed'
#     COMPLETED = 'completed'


# class Task:
#     def __init__(self, input_fileset, output_fileset_name=None, params=None):
#         self._input_fileset = input_fileset
#         self._output_fileset_name = output_fileset_name
#         self._params = params
#         self._canceled = False
#         self._progress = 0
#         self._status = TaskStatus.IDLE

#     def input_fileset(self):
#         return self._input_fileset
    
#     def has_param(self, name):
#         if self._params is not None:
#             return name in self._params.keys()
#         return False
    
#     def params(self):
#         return self._params
    
#     def param(self, name, default=None):
#         if self.has_param(name):
#             return self._params[name]
#         return default
    
#     def is_canceled(self):
#         return self._canceled
    
#     def cancel(self):
#         self._canceled = True

#     def execute(self):
#         print('Running task')
#         for i in range(5):
#             if self._canceled:
#                 self.set_status(TaskStatus.CANCELED)
#                 print('Task cancelled')
#                 return 
#             time.sleep(1)
#             self.set_progress(i, 5)
#             print(f'Task iteration {i} finished')

#     def run(self):
#         self.set_status(TaskStatus.RUNNING)
#         try:
#             self.execute()
#             if not self.is_canceled():
#                 self.set_status(TaskStatus.COMPLETED)
#         except Exception as e:
#             self.set_status(TaskStatus.FAILED)

#     def set_progress(self, step, nr_steps):
#         self._progress = int(((step + 1) / (nr_steps)) * 100)

#     def set_status(self, status, message=None):
#         self._status = status