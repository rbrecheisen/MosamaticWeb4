import os
import yaml

# from ..managers.logmanager import LogManager

# LOG = LogManager()


class Pipeline:
    def __init__(self, config_yaml_or_dict):
        self._input_dir = None
        self._tasks = []
        self._current_task_idx = 0
        self.load_config(config_yaml_or_dict)

    def add_task(self, task):
        self._tasks.append(task)

    def load_config(self, config_yaml_or_dict):
        if isinstance(config_yaml_or_dict, dict):
            pass
        else:
            self.load_config_yaml(config_yaml_or_dict)

    def load_config_dict(self, config_dict):
        pass

    def load_config_yaml(self, config_yaml):
        # Load YAML file
        with open(config_yaml, 'r') as f:
            config = yaml.safe_load(f)
        # Check contents (especially existence of directories)
        errors = self.check_config(config)
        if len(errors) > 0:
            # LOG.info(f'ERROR: configuration file has errors:')
            for error in errors:
                print(f' - {error}')
            return
        # Get input directory for pipeline and count the number of files
        self._input_dir = config['input_dir']
        if self._input_dir is None:
            raise RuntimeError(f'Pipeline has no input directory!')
        # Load task instances. When we run tasks through the pipeline the 
        # output directory names will be prepended with an index
        self._tasks = []
        for task_config in config['tasks']:
            class_name = task_config['class']
            module_name = f'mosamaticdesktop.tasks.{class_name.lower()}.{class_name.lower()}'
            input_dir = task_config['input_dir']
            # The first task may not have an input directory. In that case, take the main
            # pipeline input directory
            if not input_dir:
                # LOG.info(f'Pipeline.load_config() task {class_name} has no input directory. Using pipeline input directory...')
                input_dir = self._input_dir
            output_dir_name = task_config['output_dir_name']
            params = task_config['params']
            module = importlib.import_module(module_name)
            task_class = getattr(module, class_name)
            task = task_class(input_dir, output_dir_name, params)
            self._tasks.append(task)

    def run(self):
        for task in self._tasks:
            task.run()

# import os
# import yaml
# import importlib

# from PySide6.QtCore import QThread, Signal

# from mosamaticdesktop.tasks.taskregistry import TASK_REGISTRY
# from mosamaticdesktop.utils import LOGGER


# class Pipeline(QThread):
#     progress = Signal(int)
#     status = Signal(str)

#     def __init__(self, config_file, main_window=None):
#         super(Pipeline, self).__init__()
#         self._input_dir, self._tasks = None, []
#         self.load_config(config_file)
#         self._main_window = main_window
#         self._current_task_index = 0

#     def check_config(self, config):
#         errors = []
#         if 'input_dir' not in config.keys():
#             errors.append('Entry "input_dir" missing')
#             return errors
#         input_dir = config['input_dir']
#         if not os.path.exists(input_dir):
#             errors.append(f'Input directory {input_dir} does not exist')
#             return errors
#         # Check there are tasks defined in the pipeline                
#         if 'tasks' not in config.keys():
#             errors.append('Entry "tasks" missing')
#             return errors
#         # Check each task's configuration
#         for task_config in config['tasks']:            
#             if 'class' not in task_config.keys():
#                 errors.append(f'Task "class" entry missing ({task_config})')
#                 continue
#             class_name = task_config['class']
#             if class_name not in TASK_REGISTRY.keys():
#                 errors.append(f'Task {class_name} not in TASK_REGISTRY')
#                 continue
#             if 'input_dir' not in task_config.keys():
#                 errors.append(f'Task {class_name} "input_dir" entry missing (can be empty so it is set to the pipeline input directory)')
#                 continue
#             if 'output_dir_name' not in task_config.keys():
#                 errors.append(f'Task {class_name} "output_dir_name" entry missing')
#                 continue
#             if 'params' not in task_config.keys():
#                 errors.append(f'Task {class_name} "params" entry missing (can be empty)')
#                 continue
#         return errors

#     def load_config(self, config_file):
#         # Load YAML file
#         with open(config_file, 'r') as f:
#             config = yaml.safe_load(f)
#         # Check contents (especially existence of directories)
#         errors = self.check_config(config)
#         if len(errors) > 0:
#             LOGGER.info(f'ERROR: configuration file has errors:')
#             for error in errors:
#                 print(f' - {error}')
#             return
#         # Get input directory for pipeline and count the number of files
#         self._input_dir = config['input_dir']
#         if self._input_dir is None:
#             raise RuntimeError(f'Pipeline has no input directory!')
#         # Load task instances. When we run tasks through the pipeline the 
#         # output directory names will be prepended with an index
#         self._tasks = []
#         for task_config in config['tasks']:
#             class_name = task_config['class']
#             module_name = f'mosamaticdesktop.tasks.{class_name.lower()}.{class_name.lower()}'
#             input_dir = task_config['input_dir']
#             # The first task may not have an input directory. In that case, take the main
#             # pipeline input directory
#             if not input_dir:
#                 LOGGER.info(f'Pipeline.load_config() task {class_name} has no input directory. Using pipeline input directory...')
#                 input_dir = self._input_dir
#             output_dir_name = task_config['output_dir_name']
#             params = task_config['params']
#             module = importlib.import_module(module_name)
#             task_class = getattr(module, class_name)
#             task = task_class(input_dir, output_dir_name, params)
#             self._tasks.append(task)

#     def run(self):
#         for step in range(len(self._tasks)):
#             if self._main_window:
#                 self._tasks[step].log.connect(self._main_window.update_task_log)
#                 self._tasks[step].finished.connect(self.run_next_task) # Let task notify listeners that it's finished before moving on to next task
#             else:
#                 self._tasks[step].run()
#         if self._main_window:
#             self._current_task_index = 0
#             self.run_next_task()

#     def run_next_task(self):
#         if self._current_task_index < len(self._tasks):
#             task = self._tasks[self._current_task_index]
#             self._current_task_index += 1
#             task.start()

#     def update_input_dir(self, input_dir):
#         self._input_dir = input_dir
#         self._tasks[0]._input_dir = self._input_dir