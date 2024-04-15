from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TournamentForm, PlayerForm
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
def edit(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    players = Chess_Player.objects.filter(tournament=tournament)

    if request.method == 'POST':
        if 'tournament_form' in request.POST:
            tournament_form = TournamentForm(request.POST,instance=tournament)
            if tournament_form.is_valid():
                tournament_form.save()
                player_form = PlayerForm()
        elif 'player_form' in request.POST:
            player_form = PlayerForm(request.POST)
            if player_form.is_valid():
                player=player_form.save(commit=False)
                player.tournament=tournament
                player.save()
            tournament_form = TournamentForm(instance=tournament)

        if player_form.errors or tournament_form.errors:
            print(player_form.errors)
            print(tournament_form.errors)
            
    else:
        tournament_form = TournamentForm(instance=tournament)
        player_form = PlayerForm()

    return render(request, 'chesstour/edit.html', {
        'tournament': tournament,
        'players': players,
        'tournament_form': tournament_form,
        'player_form': player_form
    })
    
