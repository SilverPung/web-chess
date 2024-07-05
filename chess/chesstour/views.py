from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TournamentForm, PlayerForm, ScoreForm
from .models import Chess_Tournament,Chess_Game,Chess_Player
from django.db.models import Max
from django.forms import modelformset_factory
import logging
from .create_algorythms import create_game_version1,create_game_version2,determine_white_player
# Create your views here.
@login_required
def create_new(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            new_tournament = form.save()
            new_tournament_id = new_tournament.id
            print(new_tournament_id)  # prints the id of the newly created tournament
            return redirect('chesstour:edit', pk=new_tournament_id)
        else:
            print(form.errors)
    else:
        form=TournamentForm()
    return render(request, 'chesstour/create_new.html', {'form': form})

@login_required
def edit(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    if tournament.created_by != request.user:
        return redirect('core:manage')
    players = Chess_Player.objects.filter(tournament=tournament).order_by('-rating')
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
    
@login_required
def game(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    if tournament.created_by != request.user:
        return redirect('core:manage')
    games = Chess_Game.objects.filter(tournament=tournament)
    players = Chess_Player.objects.filter(tournament=tournament).order_by('-rating')
    return render(request, 'chesstour/game.html', {'tournament': tournament, 'games': games, 'players': players})

@login_required
def edit_game(request, pk):
    
    tournament = Chess_Tournament.objects.get(pk=pk)
    if tournament.created_by != request.user:#security check
        return redirect('core:manage')
    players = Chess_Player.objects.filter(tournament=tournament)
    games = Chess_Game.objects.filter(tournament=tournament)
    sorted_players = Chess_Player.objects.filter(tournament=tournament).order_by('-rating')
    
    repeater=0#variable for swithcing the starting from where to start pairing players
    while repeater<len(sorted_players):
        try: #trying to create new games with basic algorithm but if it fails wi will switch to another one
            if not games:
                create_game_version2(players,games,tournament.rounds,reapeter=repeater)
                break
            else:
                max_round = games.aggregate(Max('round'))['round__max']#checking if we already have games from previous rounds
                if tournament.rounds==max_round:
                    create_game_version2(players,games,tournament.rounds,reapeter=repeater)
                break
        except Exception as e1:
            repeater+=1
            logging.error(e1)
        if repeater==len(sorted_players)-1:#exception if algorithm cannnot create game because of loop  create by giving the same results
            Chess_Game.objects.filter(tournament=tournament).delete()
            repeater=0
            continue

    
    determine_white_player(tournament=tournament, round=tournament.rounds+1) #determining white player for each game
    current_games = Chess_Game.objects.filter(tournament=tournament,round=tournament.rounds+1)
    score_forms = [(game, ScoreForm(prefix=str(game.player1.id) + "_"+str(game.player2.id))) for game in current_games]
    
    if request.method == 'POST':
        score_forms = [(game, ScoreForm(request.POST, prefix=str(game.player1.id) + "_"+str(game.player2.id))) for game in current_games]
        for game, form in score_forms:
            if form.is_valid():
                game.player1.rating += float(form.cleaned_data['player1_score'])
                game.player1.save()
                game.player2.rating += float(form.cleaned_data['player2_score'])
                game.player2.save()
                
        tournament.rounds += 1
        tournament.save()
        return redirect('chesstour:game', pk=pk)

    return render(request, 'chesstour/edit_game.html', {'tournament': tournament, 'games': current_games, 'score_forms':score_forms, 'players': sorted_players})

@login_required              
def manage_players(request, pk,spk):
    
    if Chess_Tournament.objects.get(pk=pk).created_by!=request.user:
        return redirect('core:manage')
    
    player=Chess_Player.objects.get(pk=spk)
    form=PlayerForm(instance=player)
    if request.method == 'POST':
        form=PlayerForm(request.POST,instance=player)
        if form.is_valid():
            form.save()
            return redirect('chesstour:edit', pk=pk)
        else:
            print(form.errors)
    return render(request, 'chesstour/manage_players.html', {'form': form, 'player': player})

@login_required
def view_results(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    if tournament.created_by != request.user:
        return redirect('core:manage')
    players = Chess_Player.objects.filter(tournament=tournament).order_by('-rating')
    if players.count() < 3:
        return redirect('chesstour:edit', pk=pk)
    first = players[0]
    second = players[1]
    third = players[2]
    players=players[3:]
    if request.method == 'POST':
        tournament.delete()
        return redirect('core:manage')

    return render(request, 'chesstour/view_results.html', {'tournament': tournament, 'players': players, 'first': first, 'second': second, 'third': third})