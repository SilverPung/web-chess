from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TournamentForm

# Create your views here.
def create_new(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TournamentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('chesstour:edit')
            else:
                print(form.errors)
        else:
            form=TournamentForm()
        return render(request, 'chesstour/create_new.html', {'form': form})
    else:
        return redirect('core:login')


def edit(request):
    if request.user.is_authenticated:
        return render(request, 'chesstour/edit.html')
    else:
        return redirect('core:login')