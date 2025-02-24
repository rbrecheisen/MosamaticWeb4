import threading
import shutil
import time
import queue
import os

INPUT_DIR = '/Users/ralph/Desktop/downloads/pancreasdemo'
OUTPUT_DIR = '/Users/ralph/Desktop/downloads/pancreasdemo-output'


class Task(threading.Thread):
    def __init__(self, input_dirs, output_dir, params, queue):
        super(Task, self).__init__()
        self._input_dirs = input_dirs
        self._output_dir = output_dir
        self._params = params
        self._queue = queue
        self._canceled_event = threading.Event()

    def run(self):
        for i in range(5):
            if self._canceled_event.is_set():
                print('Task canceled')
                break
            print(f'Iteration {i}')
            time.sleep(2)
        print('Finished')

    def cancel(self):
        self._canceled_event.set()


class CopyFilesTask(Task):
    def run(self):
        input_dir = self._input_dirs[0]
        output_dir = self._output_dir
        os.makedirs(output_dir, exist_ok=True)
        files = os.listdir(input_dir)
        output_files = []
        nr_steps = len(files)
        for step in range(nr_steps):
            source = os.path.join(input_dir, files[step])
            target = os.path.join(output_dir, files[step])
            shutil.copy(source, target)
            output_files.append(target)
            print(f'Copied {source} to {target}')
            time.sleep(1)
        self._queue.put(output_files)


class TaskManager:
    def __init__(self):
        self._running_task = None
        self._queue = queue.Queue()

    def run_task(self):
        """ Task manager knows which inputs the task needs and can create
        an output fileset to obtain the output directory for the task. 
        """
        self._running_task = CopyFilesTask([INPUT_DIR], OUTPUT_DIR, None, self._queue)
        self._running_task.start()
        self._running_task.join()
        print(f'Task result: {self._queue.get()}')

    def cancel_task(self):
        self._running_task.cancel()
        self._running_task = None


def main():
    manager = TaskManager()
    manager.run_task()
    time.sleep(3)
    manager.cancel_task()


if __name__ == '__main__':
    main()