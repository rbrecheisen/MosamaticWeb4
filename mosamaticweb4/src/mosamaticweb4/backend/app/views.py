from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('/')
