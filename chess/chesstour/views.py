from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TournamentForm, PlayerForm, ScoreForm
from .models import Chess_Tournament,Chess_Game,Chess_Player
from django.db.models import Max
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
    
def check_if_in_games(player1,player2,games):
    for game in games:
        if game.player1==player1 and game.player2==player2:
            return True
        if game.player1==player2 and game.player2==player1:
            return True
    return False

def create_game(players,games,number_of_rounds):
    sorted_players=list(players.order_by('-rating'))
    #print(sorted_players)
    if len(sorted_players)%2!=0:
        bye=sorted_players[-1]
        Chess_Game.objects.create(player1=bye,player2=bye,tournament=bye.tournament,round=number_of_rounds+1)
        sorted_players=sorted_players[:-1]
    while len(sorted_players)>0:
        j=0
        while check_if_in_games(sorted_players[0],sorted_players[j+1],games):
            j+=1
            if j>=len(sorted_players)-1:
                game=games[0]
                Chess_Game.objects.filter(tournament=game.tournament).delete()
                games=[]
                j=1
                break
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)
        


def game(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    games = Chess_Game.objects.filter(tournament=tournament)
    players = Chess_Player.objects.filter(tournament=tournament)
    return render(request, 'chesstour/game.html', {'tournament': tournament, 'games': games, 'players': players})

def edit_game(request, pk):
    tournament = Chess_Tournament.objects.get(pk=pk)
    players = Chess_Player.objects.filter(tournament=tournament)
    games = Chess_Game.objects.filter(tournament=tournament)
    if not games:
        create_game(players,games,tournament.rounds)
    else:
        max_round = games.aggregate(Max('round'))['round__max']
        if tournament.rounds==max_round:
            create_game(players,games,tournament.rounds)
        

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

    return render(request, 'chesstour/edit_game.html', {'tournament': tournament, 'games': current_games, 'score_forms':score_forms})
                
            
   