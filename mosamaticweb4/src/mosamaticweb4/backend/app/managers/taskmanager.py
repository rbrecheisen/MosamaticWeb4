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
        self._curret_task_queue = None

    def run_task_from_request(self, task_name, request):
        """ Collect input fileset IDs and parameters from request object and 
        run task with given name.
        """
        manager = DataManager()
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:            
            input_filesets = {}
            for fileset_name in task_info['input_filesets']:
                fileset_id = request.POST.get(fileset_name, None)
                if fileset_id:
                    fs = manager.get_fileset(fileset_id)
                    input_filesets[fileset_name] = fs
            output_fileset_name = task_info['output_files']
            output_fileset = manager.create_fileset(request.user, output_fileset_name)
            params = {}
            for param_name in task_info['params']:
                param_value = request.POST.get(param_name, None)
                if param_value:
                    params[param_name] = param_value
            self.run_task(task_name, input_filesets, params, output_fileset.path)
        else:
            LOG.error(f'Could not find class for task {task_name} in TASK_REGISTRY')

    def run_task(self, task_name, input_filesets, params, output_fileset_path):
        """ Runs task with given name, input filesets and parameters"""
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            self._curret_task_queue = queue.Queue()
            task_class = task_info['class']
            self._current_task = task_class(input_filesets, params)
            self._current_task.start()

    def get_current_task(self):
        """ Returns currently running task"""
        return self._current_task
    
    def cancel_current_task(self):
        """ Cancels currently running task"""
        if self._current_task:
            self._current_task.cancel()

    def get_progress_current_task(self):
        """ Returns progress of currently running task"""
        if self._current_task:
            return self._current_task.progress()
        
    def get_status_current_task(self):
        """ Returns status of currently running task"""
        if self._current_task:
            return self._current_task.status()
        
    def remove_current_task(self):
        """ Sets currently running task object to None, effectively removing it"""
        self._current_task = None


    # def run_pipeline(self):
    #     pipeline = Pipeline({})
    #     pipeline.add_task(Task(None, None, None))
    #     pipeline_thread = threading.Thread(target=pipeline.run)
    #     pipeline_thread.start()