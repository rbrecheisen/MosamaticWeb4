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

        # Initialize data manager
        manager = DataManager()

        # Get task info from task registry based on task name
        task_info = TASK_REGISTRY.get(task_name, None)

        if task_info:

            # Retrieve input filesets by getting their IDs from the 
            # request object and retrieving the filesets with the
            # data manager
            input_dirs = {}
            for fileset_name in task_info['input_fileset_names']:
                fileset_id = request.POST.get(fileset_name, None)
                if fileset_id:
                    fs = manager.get_fileset(fileset_id)
                    input_dirs[fileset_name] = fs.path()

            # Create output fileset and get its directory. This will be passed to
            # task later as output directory
            output_fileset_name = task_info['output_fileset_name']
            self._current_output_fileset = manager.create_fileset(request.user, output_fileset_name)
            output_dir = self._current_output_fileset.path()

            # Retrieve task parameters
            params = {}
            for param_name in task_info['params']:
                param_value = request.POST.get(param_name, None)
                if param_value:
                    params[param_name] = param_value

            # Run task with given input directories, output directory and parameters
            self.run_task(task_name, input_dirs, output_dir, params)
        else:
            LOG.error(f'Could not find class for task {task_name} in TASK_REGISTRY')

    def run_task(self, task_name, input_dirs, output_dir, params):

        # Get task info from task registry
        task_info = TASK_REGISTRY.get(task_name, None)

        if task_info:

            # Create a new (task-specific) queue object
            self._queue = queue.Queue()

            # Get task class and instantiate it using the input directories, output
            # directory and parameters. Also, pass queue object and a callback
            # function to notify the task manager that the task has finished
            task_class = task_info['class']
            self._current_task = task_class(
                input_dirs, output_dir, params, self._queue, self.current_task_finished)
            
            # Start the task in the background
            self._current_task.start()

    def get_current_task(self):
        return self._current_task
    
    def cancel_current_task(self):
        if self._current_task:
            self._current_task.cancel()

    def current_task_finished(self):
        if self._queue:
            manager = DataManager()
            file_paths = self._queue.get()

            # Run through list of task output files and create FileModel
            # object for each using output fileset created earlier
            for file_path in file_paths:
                manager.create_file(file_path, self._current_output_fileset)
        
    def remove_current_task(self):
        self._current_task = None
        self._current_output_fileset = None

    # def run_pipeline(self):
    #     pipeline = Pipeline({})
    #     pipeline.add_task(Task(None, None, None))
    #     pipeline_thread = threading.Thread(target=pipeline.run)
    #     pipeline_thread.start()