from ..tasks.taskregistry import TASK_REGISTRY
from .datamanager import DataManager
from .logmanager import LogManager
from ..singleton import singleton

LOG = LogManager()


@singleton
class TaskManager:
    def __init__(self):
        self._current_task = None

    def run_task_from_request(self, task_name, request):
        manager = DataManager()
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:            
            input_filesets = []
            for fileset_name in task_info['input_filesets']:
                fileset_id = request.POST.get(fileset_name, None)
                if fileset_id:
                    fs = manager.get_fileset(fileset_id)
                    input_filesets.append(fs)
            params = {}
            for param_name in task_info['params']:
                param_value = request.POST.get(param_name, None)
                if param_value:
                    params[param_name] = param_value
            self.run_task(task_name, input_filesets, params)
        else:
            LOG.error(f'Could not find class for task {task_name} in TASK_REGISTRY')

    def run_task(self, task_name, input_filesets, params):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            self._current_task = task_info['class'](input_filesets, params, self)
            self._current_task.start()

    def cancel_current_task(self):
        if self._current_task:
            self._current_task.cancel()

    def get_progress_current_task(self):
        if self._current_task:
            return self._current_task.progress()
        
    def get_status_current_task(self):
        if self._current_task:
            return self._current_task.status()
        
    def get_current_task(self):
        return self._current_task
    
    def remove_current_task(self):
        self._current_task = None


    # def run_pipeline(self):
    #     pipeline = Pipeline({})
    #     pipeline.add_task(Task(None, None, None))
    #     pipeline_thread = threading.Thread(target=pipeline.run)
    #     pipeline_thread.start()