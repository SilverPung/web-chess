from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TournamentForm
from .models import Chess_Tournament,Chess_Game,Chess_Player
# Create your views here.
@login_required
def create_new(request):
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

@login_required
def edit(request,pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    games = Chess_Game.objects.filter(tournament=tournament)
    player = Chess_Player.objects.filter(tournament=tournament)
    return render(request, 'chesstour/edit.html', {'tournament': tournament,'games':games,'player':player})
    
