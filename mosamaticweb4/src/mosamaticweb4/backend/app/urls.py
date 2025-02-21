from django.urls import path

from .views import custom_logout, filesets, fileset, logs, tasks, task, pipeline


urlpatterns = [
    path('', filesets),
    path('filesets/', filesets),
    path('filesets/<str:fileset_id>', fileset),
    path('tasks/', tasks),
    path('tasks/<str:task_name>', task),
    path('pipeline/', pipeline),
    path('accounts/logout/', custom_logout, name='logout'),
    path('logs/', logs),
]