import threading

from ..tasks.task import Task
from ..tasks.pipeline import Pipeline
from ..tasks.taskregistry import TASK_REGISTRY


class TaskManager:
    def __init__(self):
        self._tasks = []

    def get_task_names(self):
        return TASK_REGISTRY.keys()

    def run_task(self, name):
        task_class = TASK_REGISTRY.get(name, None)
        if task_class is not None:
            task = task_class() # Where do inputs and outputs come from?
            task_thread = threading.Thread(target=task.run)
            task_thread.start()

    def run_pipeline(self):
        pipeline = Pipeline({})
        pipeline.add_task(Task(None, None, None))
        pipeline_thread = threading.Thread(target=pipeline.run)
        pipeline_thread.start()