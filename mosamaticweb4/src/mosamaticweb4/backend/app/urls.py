from django.urls import path

from .views import custom_logout, filesets, fileset, logs


urlpatterns = [
    path('', filesets),
    path('filesets/', filesets),
    path('filesets/<str:fileset_id>', fileset),
    path('logs/', logs),
    path('accounts/logout/', custom_logout, name='logout'),
]