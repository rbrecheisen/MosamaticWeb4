import queue

from ..tasks.taskregistry import TASK_REGISTRY
from .datamanager import DataManager
from .logmanager import LogManager
from ..singleton import singleton

LOG = LogManager()


@singleton
class TaskManager:
    def __init__(self):
        self._current_task = None
        self._current_output_fileset = None
        self._queue = None

    def run_task_from_request(self, task_name, request):
        manager = DataManager()
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:            
            # Retrieve input filesets
            input_dirs = {}
            for fileset_name in task_info['input_filesets']:
                fileset_id = request.POST.get(fileset_name, None)
                if fileset_id:
                    fs = manager.get_fileset(fileset_id)
                    input_dirs[fileset_name] = fs.path
            # Create output fileset
            output_fileset_name = task_info['output_fileset']
            self._current_output_fileset = manager.create_fileset(request.user, output_fileset_name)
            output_dir = self._current_output_fileset.path
            # Retrieve task parameters
            params = {}
            for param_name in task_info['params']:
                param_value = request.POST.get(param_name, None)
                if param_value:
                    params[param_name] = param_value
            # Run task
            self.run_task(task_name, input_dirs, output_dir, params)
        else:
            LOG.error(f'Could not find class for task {task_name} in TASK_REGISTRY')

    def run_task(self, task_name, input_dirs, output_dir, params):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            self._queue = queue.Queue()
            task_class = task_info['class']
            self._current_task = task_class(input_dirs, output_dir, params, self._queue)
            self._current_task.start()

    def get_current_task(self):
        return self._current_task
    
    def cancel_current_task(self):
        if self._current_task:
            self._current_task.cancel()

    def get_result_current_task(self):
        if self._queue:
            return self._queue.get()
        
    def remove_current_task(self):
        self._current_task = None

    # def run_pipeline(self):
    #     pipeline = Pipeline({})
    #     pipeline.add_task(Task(None, None, None))
    #     pipeline_thread = threading.Thread(target=pipeline.run)
    #     pipeline_thread.start()