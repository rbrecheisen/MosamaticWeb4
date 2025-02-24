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
    def __init__(self, input_filesets, params):
        super(Task, self).__init__()
        self._name = self.__class__.__name__
        self._input_filesets = input_filesets
        self._params = params
        self._cancel_event = threading.Event()
        self._progress = 0
        self._status = TaskStatus.IDLE

    # PROPERTIES

    @property
    def name(self):
        return self._name
    
    @property
    def input_filesets(self):
        fileset_names = []
        for fs in self._input_filesets.values():
            fileset_names.append(fs.name)
        return fileset_names
    
    @property
    def params(self):
        return self._params

    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status.value
    
    # FUNCTIONS

    def input_fileset(self, name):
        if name in self._input_filesets.keys():
            return self._input_filesets[name]
        return None

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

    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        LOG.info(f'{self.__class__.__name__}: progress = {self._progress}')

    def set_status(self, status, message=None):
        self._status = status
        LOG.info(f'{self.__class__.__name__}: status = {status.value} ({message})')