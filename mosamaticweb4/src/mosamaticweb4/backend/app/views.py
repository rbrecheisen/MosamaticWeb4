import os

from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseForbidden
from wsgiref.util import FileWrapper

from .managers.datamanager import DataManager
from .managers.logmanager import LogManager
from .managers.taskmanager import TaskManager

LOG = LogManager()


@login_required
def filesets(request):
    manager = DataManager()
    if request.method == 'POST':
        fileset_name = request.POST.get('fileset_name', None)
        files = request.FILES.getlist('files')
        if len(files) > 0:
            fileset = manager.create_fileset(request.user, fileset_name)
            LOG.info(f'Created new fileset {fileset.name} with {len(files)} files')
            for f in files:
                f_path = os.path.join(str(fileset.id), f.name)
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
                response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(fileset.name)
            LOG.info(f'Created ZIP archive for fileset {fileset.name} ({zip_file_path})')
            return response
        elif action == 'delete':
            manager.delete_fileset(fileset)
            LOG.info(f'Deleted fileset {fileset.name}')
            return render(request, 'filesets.html', context={'filesets': manager.get_filesets(request.user)})
        elif action == 'rename':
            new_name = request.GET.get('new_name')
            fileset = manager.rename_fileset(fileset, new_name)
            LOG.info(f'Renamed fileset {fileset.name} to {new_name}')
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
    manager = TaskManager()
    return render(request, 'tasks.html', context={'task_names': manager.get_task_names()})


@login_required
def task(request, task_name):
    if request.method == 'POST':
        manager = TaskManager()
        manager.run_task(task_name)
        return render(request, 'tasks.html', context={'tasks': []})
    manager = DataManager()
    return render(request, f'tasks/{task_name}.html', context={
        'filesets': manager.get_filesets(request.user)
    })


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
