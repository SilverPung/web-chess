from django.test import TestCase
from .models import Chess_Player, Chess_Game, Chess_Tournament
from .views import create_game
from django.contrib.auth.models import User

class CreateGameTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tournament = Chess_Tournament.objects.create(name='Test Tournament', description='Test Description',created_by_id=1)
        Chess_Player.objects.create(name='Player 1',surname='Player1',tournament=self.tournament, rating=1),
        Chess_Player.objects.create(name='Player 2',surname='Player2', tournament=self.tournament, rating=0),
        Chess_Player.objects.create(name='Player 3',surname='Player3',tournament=self.tournament, rating=2),
        Chess_Player.objects.create(name='Player 4',surname='Player4',tournament=self.tournament, rating=1),
        self.players = Chess_Player.objects.filter(tournament=self.tournament)

    def test_create_game(self):
        create_game( self.players , [], 0)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((self.players[0], self.players[2])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((self.players[3], self.players[1])))

    def test_create_game_with_bye(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 4])
        create_game(players, [], 0)
        games = Chess_Game.objects.all()
        #print(games)
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[1], players[1])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[0], players[2])))
    def test_create_game_with_previous_games(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game(players, [], 0)
        games = Chess_Game.objects.all()
        create_game(players, games, 1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[2], players[3])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[0], players[1]))
        )
    def test_create_game_with_previous_games_and_changing_score(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game(players, [], 0)
        games = Chess_Game.objects.all()
        Chess_Player.objects.filter(id=1).update(rating=2)
        Chess_Player.objects.filter(id=4).update(rating=2)
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game(players, games, 1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[0], players[3])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[1], players[2]))
        )