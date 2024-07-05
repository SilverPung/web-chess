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

def create_game_version1(players,games,number_of_rounds):#dead algoritm not used anymore 

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
        
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        to_create.append((player1,player2))
    for player1,player2 in to_create:
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)

def create_game_version2(players,games,number_of_rounds,reapeter=1): #new algorithm for creating games
    sorted_players=list(players.order_by('-rating'))
    #print(sorted_players)
    to_create=[]
    
    if len(sorted_players)%2!=0: #if there is odd number of players
        bye=sorted_players[-1]
        to_create.append((bye,bye))
        sorted_players=sorted_players[:-1]
    
    while len(sorted_players)>0:
        j=reapeter
        
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
                j=reapeter
        
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        to_create.append((player1,player2))
    for player1,player2 in to_create:
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)

def determine_white_player(tournament, round):
    games=Chess_Game.objects.filter(tournament=tournament,round=round)
    for game in games:
        if game.white_player==None:
            if game.player1.white_games>game.player2.white_games:
                game.white_player=game.player2
                game.player2.white_games+=1
            else:
                game.white_player=game.player1
                game.player1.white_games+=1
            game.player1.save()
            game.player2.save()
            game.save()


def creating_game_version3(players,games,number_of_rounds):

    sorted_players=list(players.order_by('-rating'))
    #print(sorted_players)
    to_create={}
    
    repeater=0
    
    if len(sorted_players)%2!=0: #if there is odd number of players
        bye=sorted_players[-1]
        to_create.update({repeater:(bye,bye)})
        repeater+=1
        sorted_players=sorted_players[:-1]
    j=0
    #repeater=0/1
    while len(sorted_players)>0:
        try:
            while check_if_in_games(sorted_players[0],sorted_players[j+1],games):
                j+=1
        except IndexError: 
            if len(to_create)==0:
                game=games[0]
                Chess_Game.objects.filter(tournament=game.tournament).delete()
            else:
                repeater-=1
                player1,player2=to_create.pop(repeater)
                sorted_players.insert(0,player1)
                sorted_players.insert(1,player2)
                j=1
                continue
        
        player1=sorted_players[0]
        player2=sorted_players[j+1]
        sorted_players.remove(player1)
        sorted_players.remove(player2)
        to_create.update({repeater:(player1,player2)})
        repeater+=1
        j=0 
    for key,value in to_create.items():
        player1,player2=value
        Chess_Game.objects.create(player1=player1,player2=player2,tournament=player1.tournament,round=number_of_rounds+1)

