import threading

from ..tasks.taskregistry import TASK_REGISTRY


class TaskManager:
    def __init__(self):
        pass

    def run_task(self, task_name, input_filesets, params):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            task = task_info['class'](input_filesets, params)
            task_thread = threading.Thread(target=task.run)
            task_thread.start()

    # def run_pipeline(self):
    #     pipeline = Pipeline({})
    #     pipeline.add_task(Task(None, None, None))
    #     pipeline_thread = threading.Thread(target=pipeline.run)
    #     pipeline_thread.start()