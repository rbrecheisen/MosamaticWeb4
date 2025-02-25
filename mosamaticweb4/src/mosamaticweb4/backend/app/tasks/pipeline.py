import threading
import queue

from ..managers.taskmanager import TaskManager


class Pipeline(threading.Thread):
    def __init__(self, config=None):
        super(Pipeline, self).__init__()
        self._config = {
            'input_dir': '/Users/ralph/Desktop/downloads/pancreasdemo',
            'tasks': {
                'DecompressDicomFilesTask': {
                    'input_fileset_names': {
                        'fileset': None,
                    },
                    'output_fileset_name': 'decompressdicomfilestask',
                    'params': None,
                },
            }
        }

    def run(self):
        input_dir = self._config['input_dir']
        for task_name in self._config['tasks'].keys():
            task_info = self._config['tasks'][task_name]
            input_dirs = []
            for input_fileset_name in task_info['input_fileset_names'].keys():
                task_input_dir = task_info['input_fileset_names'][input_fileset_name]
                if task_input_dir is None:
                    task_input_dir = input_dir
                input_dirs.append(task_input_dir)
            output_dir_name = task_info['output_fileset_name']

