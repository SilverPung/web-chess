from .models import Chess_Game
from django.db.models import Max
import logging
# Create your views here.




def check_if_in_games(player1,player2,games):
    for game in games:
        if game.player1==player1 and game.player2==player2:
            return True
        if game.player1==player2 and game.player2==player1:
            return True
    return False

def create_game_version1(players,games,number_of_rounds):#algorithm to make pairs of players

    sorted_players=list(players.order_by('-rating'))
    #print(sorted_players)
    to_create=[]
    
    if len(sorted_players)%2!=0:
        bye=sorted_players[-1]
        to_create.append((bye,bye))
        sorted_players=sorted_players[:-1]
    
    while len(sorted_players)>0:
        j=0
        
        try:
            while check_if_in_games(sorted_players[0],sorted_players[j+1],games):
                j+=1
        except IndexError :#if there is only one pair left and they can't play with each other
            if to_create:
                to_create=[]
                raise Exception("Can't create a game with this algorithm(1)")
            else:#if all players have played with each other
                game=games[0]
                Chess_Game.objects.filter(tournament=game.tournament).delete()
                games=[]
                j=0
                continue
        
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        to_create.append((player1,player2))
    for player1,player2 in to_create:
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)

def create_game_version2(players,games,number_of_rounds):
    sorted_players=list(players.order_by('-rating'))
    #print(sorted_players)
    to_create=[]
    
    if len(sorted_players)%2!=0:
        bye=sorted_players[-1]
        to_create.append((bye,bye))
        sorted_players=sorted_players[:-1]
    
    while len(sorted_players)>0:
        j=1
        
        try:
            while check_if_in_games(sorted_players[0],sorted_players[j+1],games):
                j+=1
        except IndexError:
            if not check_if_in_games(sorted_players[0],sorted_players[1],games):
                j=0
            elif to_create:#if there is only one pair left and they can't play with each other
                to_create=[]
                raise Exception("Can't create a game with this algorithm(2)")
            else:#if all players have played with each other
                game=games[0]
                Chess_Game.objects.filter(tournament=game.tournament).delete()
                games=[]
                j=1
        
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        to_create.append((player1,player2))
    for player1,player2 in to_create:
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)