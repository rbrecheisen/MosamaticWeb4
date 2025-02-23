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
    def __init__(self, input_dirs, output_dir, params, queue):
        super(Task, self).__init__()
        self._name = self.__class__.__name__
        self._input_dirs = input_dirs
        self._output_dir = output_dir
        self._params = params
        self._queue = queue
        self._cancel_event = threading.Event()
        self._progress = 0
        self._status = TaskStatus.IDLE

    # PROPERTIES

    @property
    def name(self):
        return self._name
    
    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status.value
    
    # FUNCTIONS

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
            self.execute()
            if not self.is_canceled():                
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            self.set_status(TaskStatus.FAILED, str(e))

    def is_canceled(self):
        return self._cancel_event.is_set()
    
    def cancel(self):
        self._cancel_event.set()
        self.set_status(TaskStatus.CANCELED)

    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        LOG.info(f'{self.__class__.__name__}: progress = {self._progress}')

    def set_status(self, status, message=None):
        self._status = status
        LOG.info(f'{self.__class__.__name__}: status = {status.value} ({message})')