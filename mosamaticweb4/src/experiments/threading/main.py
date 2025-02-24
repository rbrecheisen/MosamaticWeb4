import threading
import time


class Task(threading.Thread):
    def __init__(self):
        super(Task, self).__init__()
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


class TaskManager:
    def __init__(self):
        self._running_task = None

    def run_task(self):
        self._running_task = Task()
        self._running_task.start()
        # time.sleep(3)
        # self._running_task.cancel()

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