import os

from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseForbidden
from wsgiref.util import FileWrapper

from .data.datamanager import DataManager
from .data.logmanager import LogManager


@login_required
def filesets(request):
    manager = DataManager()
    if request.method == 'POST':
        fileset_name = request.POST.get('fileset_name', None)
        files = request.FILES.getlist('files')
        if len(files) > 0:
            fileset = manager.create_fileset(request.user, fileset_name)
            for f in files:
                f_path = os.path.join(str(fileset.id), f.name)
                default_storage.save(f_path, ContentFile(f.read()))
                manager.create_file(f_path, fileset)
        return render(request, 'filesets.html', context={'filesets': manager.get_filesets(request.user)})
    return render(request, 'filesets.html')


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
            return response
        elif action == 'delete':
            manager.delete_fileset(fileset)
            return render(request, 'filesets.html', context={'filesets': manager.get_filesets(request.user)})
        elif action == 'rename':
            fileset = manager.rename_fileset(fileset, request.GET.get('new_name'))
        else:
            pass
        return render(request, 'fileset.html', context={'fileset': fileset, 'files': manager.get_files(fileset)})
    return HttpResponseForbidden(f'Wrong method ({request.method}) or action ({action})')


@login_required
def logs(request):
    manager = LogManager()
    if request.method == 'POST':
        manager.delete_messages()
    return render(request, 'logs.html', context={'messages': manager.get_messages()})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/')
