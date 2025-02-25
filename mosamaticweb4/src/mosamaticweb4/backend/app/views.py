import os

from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from wsgiref.util import FileWrapper

from .managers.datamanager import DataManager
from .managers.logmanager import LogManager
from .managers.taskmanager import TaskManager
from .tasks.taskregistry import TASK_REGISTRY

LOG = LogManager()


def is_auto_refresh(request):
    return True if request.GET.get('auto-refresh', '0') == '1' else False


@login_required
def filesets(request):
    manager = DataManager()
    if request.method == 'POST':
        fileset_name = request.POST.get('fileset_name', None)
        files = request.FILES.getlist('files')
        if len(files) > 0:
            fileset = manager.create_fileset(request.user, fileset_name)
            LOG.info(f'Created new fileset {fileset.name()} with {fileset.size()} files')
            for f in files:
                f_path = os.path.join(str(fileset.id()), f.name)
                default_storage.save(f_path, ContentFile(f.read()))
                manager.create_file(f_path, fileset)
                LOG.info(f'Added file {f_path} to fileset')
    return render(request, 'filesets.html', context={'filesets': manager.get_filesets(request.user)})


@login_required
def fileset(request, fileset_id):
    manager = DataManager()
    action = None
    if request.method == 'GET':
        fileset = manager.get_fileset(fileset_id)
        action = request.GET.get('action', None)
        if action == 'download':
            zip_file_path = manager.get_zip_file_from_fileset(fileset)
            with open(zip_file_path, 'rb') as f:
                response = HttpResponse(FileWrapper(f), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(fileset.name())
            LOG.info(f'Created ZIP archive for fileset {fileset.name()} ({zip_file_path})')
            return response
        elif action == 'delete':
            manager.delete_fileset(fileset)
            LOG.info(f'Deleted fileset {fileset.name()}')
            return render(request, 'filesets.html', context={'filesets': manager.get_filesets(request.user)})
        elif action == 'rename':
            new_name = request.GET.get('new_name')
            manager.rename_fileset(fileset, new_name)
            LOG.info(f'Renamed fileset {fileset.name()} to {new_name}')
        else:
            pass
        return render(request, 'fileset.html', context={'fileset': fileset, 'files': manager.get_files(fileset)})
    message = f'Wrong method ({request.method}) or action ({action})'
    LOG.error(message)
    return HttpResponseForbidden(message)


@login_required
def logs(request):
    manager = LogManager()
    if request.method == 'POST':
        manager.delete_messages()
    return render(request, 'logs.html', context={'messages': manager.get_messages()})


@login_required
def tasks(request):
    task_manager = TaskManager()
    auto_refresh = True if request.GET.get('auto-refresh', '0') == '1' else False
    if request.method == 'GET':
        remove = True if request.GET.get('remove', '0') == '1' else False
        if remove:
            task_manager.remove_current_task()
        cancel = True if request.GET.get('cancel', '0') == '1' else False
        if cancel:
            task_manager.cancel_current_task()
    current_task = task_manager.get_current_task()
    if current_task:
        if current_task.get_status() == 'completed' or current_task.get_status() == 'failed' or current_task.get_status() == 'canceled':
            auto_refresh = False
    return render(request, 'tasks.html', context={'task_names': TASK_REGISTRY.keys(), 'current_task': current_task, 'auto_refresh': auto_refresh})


@login_required
def task(request, task_name):
    data_manager = DataManager()
    if request.method == 'POST':
        task_manager = TaskManager()
        task_manager.run_task_from_request(task_name, request)
        return redirect('/tasks/')
    context = {'task_name': task_name, 'filesets': data_manager.get_filesets(request.user)}
    return render(request, f'tasks/{task_name}.html', context=context)


@login_required
def pipeline(request):
    pass


@login_required
def help(request):
    return render(request, 'help/index.html')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/')
