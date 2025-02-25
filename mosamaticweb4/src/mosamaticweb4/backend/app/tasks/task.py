import os
import threading

from enum import Enum

from ..managers.logmanager import LogManager

LOG = LogManager()


class TaskStatus(Enum):
    IDLE = 'idle'
    RUNNING = 'running'
    CANCELED = 'canceled'
    FAILED = 'failed'
    COMPLETED = 'completed'


class Task(threading.Thread):

    def __init__(self, input_dirs, output_dir, params, queue, notify_finished_callback):
        super(Task, self).__init__()
        self._name = self.__class__.__name__
        self._input_dirs = input_dirs
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)
        self._params = params
        self._queue = queue
        self._cancel_event = threading.Event()
        self._progress = 0
        self._status = TaskStatus.IDLE
        self.notify_finished = notify_finished_callback

    def get_name(self):
        return self._name
    
    def get_input_dir(self, name):
        if name in self._input_dirs.keys():
            return self._input_dirs[name]
        return None
    
    def get_output_dir(self):
        return self._output_dir

    def get_param(self, name, default=None):
        if name in self._params.keys():
            return self._params[name]
        return default
    
    def execute(self):
        raise NotImplementedError()

    def run(self):
        self.set_status(TaskStatus.RUNNING)
        try:
            # Execute child task and gets its output files
            file_paths = self.execute()
            # Check if task was canceled. If not, set its status to
            # completed, queue the output files and notify the task
            # manager that the task is finished
            if not self.is_canceled():                
                self.set_status(TaskStatus.COMPLETED)
                self._queue.put(file_paths)
                self.notify_finished()
        except Exception as e:
            self.set_status(TaskStatus.FAILED, str(e))

    def is_canceled(self):
        return self._cancel_event.is_set()
    
    def cancel(self):
        self._cancel_event.set()
        self.set_status(TaskStatus.CANCELED)

    def get_progress(self):
        return self._progress

    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        self.log_info(f'progress = {self._progress}')

    def get_status(self):
        return self._status.value
    
    def set_status(self, status, message=None):
        self._status = status
        self.log_info(f'status = {status.value} ({message})')

    def log_info(self, message):
        LOG.info(f'{self._class__.__name__}: {message}')

    def log_warning(self, message):
        LOG.warning(f'{self._class__.__name__}: {message}')

    def log_error(self, message):
        LOG.error(f'{self._class__.__name__}: {message}')