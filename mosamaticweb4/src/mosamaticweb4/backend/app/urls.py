from django.urls import path

from .views import custom_logout, filesets, fileset, logs, tasks, task, pipeline, help, file, file_to_png, file_to_text, file_to_csv


urlpatterns = [
    path('', filesets),
    path('filesets/', filesets),
    path('filesets/<str:fileset_id>', fileset),
    path('files/<str:file_id>', file),
    path('files/<str:file_id>/png', file_to_png),
    path('files/<str:file_id>/text', file_to_text),
    path('files/<str:file_id>/csv', file_to_csv),
    path('tasks/', tasks),
    path('tasks/<str:task_name>', task),
    path('pipeline/', pipeline),
    path('accounts/logout/', custom_logout, name='logout'),
    path('help/', help),
    path('logs/', logs),
]