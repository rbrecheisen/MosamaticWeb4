from django.urls import path

from .views import custom_logout, home


urlpatterns = [
    path('', home),
    path('accounts/logout/', custom_logout, name='logout'),
]