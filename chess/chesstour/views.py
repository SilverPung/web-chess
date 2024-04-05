from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def create_new(request):
    if request.user.is_authenticated:
        return render(request, 'chesstour/create_new.html')
    else:
        return redirect('core:login')


def edit(request):
    if request.user.is_authenticated:
        return render(request, 'chesstour/edit.html')
    else:
        return redirect('core:login')