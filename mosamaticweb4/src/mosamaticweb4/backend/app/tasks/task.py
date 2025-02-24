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
    def __init__(self, input_filesets, params, task_manager):
        super(Task, self).__init__()
        self._name = self.__class__.__name__
        self._input_filesets = input_filesets
        self._params = params
        self._task_manager = task_manager
        self._cancel_event = threading.Event()
        self._progress = 0
        self._status = TaskStatus.IDLE

    @property
    def name(self):
        return self._name

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

    @property
    def progress(self):
        return self._progress

    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        LOG.info(f'{self.__class__.__name__}: progress = {self._progress}')

    @property
    def status(self):
        return self._status.value

    def set_status(self, status, message=None):
        self._status = status
        LOG.info(f'{self.__class__.__name__}: status = {status.value} ({message})')