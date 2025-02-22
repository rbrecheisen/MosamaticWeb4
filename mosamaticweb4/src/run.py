from mosamaticweb4.app import main
from mosamaticweb4.backend.app.managers.taskmanager import TaskManager


if __name__ == '__main__':
    manager = TaskManager()
    # manager.run_task()
    manager.run_pipeline()
    # main()