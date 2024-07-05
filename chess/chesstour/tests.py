from django.test import TestCase
from .models import Chess_Player, Chess_Game, Chess_Tournament
from .views import create_game_version1,create_game_version2
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from unittest import mock
class CreateGameTestRepeat1(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tournament = Chess_Tournament.objects.create(name='Test Tournament', description='Test Description',created_by_id=1)
        Chess_Player.objects.create(name='Player 1',surname='Player1',tournament=self.tournament, rating=1),
        Chess_Player.objects.create(name='Player 2',surname='Player2', tournament=self.tournament, rating=0),
        Chess_Player.objects.create(name='Player 3',surname='Player3',tournament=self.tournament, rating=2),
        Chess_Player.objects.create(name='Player 4',surname='Player4',tournament=self.tournament, rating=1),
        self.players = Chess_Player.objects.filter(tournament=self.tournament)

    def test_create_game(self):
        create_game_version2( self.players , [], 0,0)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((self.players[0], self.players[2])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((self.players[3], self.players[1])))
    def test_create_game_with_bye(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 4])
        create_game_version2(players, [], 0,0)
        games = Chess_Game.objects.all()
        #print(games)
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[1], players[1])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[0], players[2])))
    def test_create_game_with_previous_games(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, [], 0,0)
        games = Chess_Game.objects.all()
        create_game_version2(players, games, 1,0)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[2], players[3])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[0], players[1]))
        )
    def test_create_game_with_previous_games_and_changing_score(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, [], 0,0)
        games = Chess_Game.objects.all()
        Chess_Player.objects.filter(id=1).update(rating=2)
        Chess_Player.objects.filter(id=4).update(rating=2)
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, games, 1,0)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[0], players[3])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[1], players[2]))
        )

class CreateGameTestRepeat2(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tournament = Chess_Tournament.objects.create(name='Test Tournament', description='Test Description',created_by_id=1)
        Chess_Player.objects.create(name='Player 1',surname='Player1',tournament=self.tournament, rating=1),#0
        Chess_Player.objects.create(name='Player 2',surname='Player2', tournament=self.tournament, rating=0),#1
        Chess_Player.objects.create(name='Player 3',surname='Player3',tournament=self.tournament, rating=2),#2
        Chess_Player.objects.create(name='Player 4',surname='Player4',tournament=self.tournament, rating=1),#3
        self.players = Chess_Player.objects.filter(tournament=self.tournament)
    
    def test_create_game(self):
        create_game_version2( self.players , [], 0,1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((self.players[2], self.players[3])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((self.players[0], self.players[1])))
    def test_create_game_with_bye(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 4])
        create_game_version2(players, [], 0,1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 2)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[1], players[1]))
        )
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[0], players[2]))
        )
    def test_create_game_with_previous_games(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, [], 0,1)
        games = Chess_Game.objects.all()
        create_game_version2(players, games, 1,1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[2], players[1])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[3], players[0]))
        )
    def test_create_game_with_previous_games_and_changing_score(self):
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, [], 0,1)
        games = Chess_Game.objects.all()
        Chess_Player.objects.filter(id=2).update(rating=1)
        Chess_Player.objects.filter(id=4).update(rating=2)
        players = Chess_Player.objects.filter(id__in=[1, 2, 3, 4])
        create_game_version2(players, games, 1,1)
        games = Chess_Game.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 4)
        #print(games)
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[2], players[0])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[1], players[3]))
        )

class TestEditGame(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tournament = Chess_Tournament.objects.create(created_by=self.user)
        Chess_Player.objects.create(name='Player 1', surname='Player1', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 2', surname='Player2', tournament=self.tournament, rating=0)
        Chess_Player.objects.create(name='Player 3', surname='Player3', tournament=self.tournament, rating=2)
        Chess_Player.objects.create(name='Player 4', surname='Player4', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 5', surname='Player5', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 6', surname='Player6', tournament=self.tournament, rating=1)
        self.players = Chess_Player.objects.filter(tournament=self.tournament)
        self.edit_game_url = reverse('chesstour:edit_game', args=[self.tournament.id])
    @mock.patch('logging.error')
    def test_edit_game_two_rounds(self, mock_log):
        self.client.login(username='testuser', password='12345')
        # Play first round
        response = self.client.post(self.edit_game_url)
        self.assertEqual(Chess_Game.objects.count(), 3)
        # Play second round
        response = self.client.post(self.edit_game_url)
        self.assertTrue(mock_log.call_count==1)
        games = Chess_Game.objects.all()
        players = Chess_Player.objects.all()
        self.assertEqual(Chess_Game.objects.count(), 6)
        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[2], players[0])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[3], players[4])))
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[5], players[1])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[2], players[3])))
        self.assertEqual(set((games[4].player1, games[4].player2)), set((players[0], players[5])))
        self.assertEqual(set((games[5].player1, games[5].player2)), set((players[4], players[1])))
        
        #print(Chess_Game.objects.all())

class TestEditGameAdvanced(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tournament = Chess_Tournament.objects.create(created_by=self.user)
        Chess_Player.objects.create(name='Player 0', surname='Player0', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 1', surname='Player1', tournament=self.tournament, rating=0)
        Chess_Player.objects.create(name='Player 2', surname='Player2', tournament=self.tournament, rating=2)
        Chess_Player.objects.create(name='Player 3', surname='Player3', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 4', surname='Player4', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 5', surname='Player5', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 6', surname='Player6', tournament=self.tournament, rating=2)
        Chess_Player.objects.create(name='Player 7', surname='Player7', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 8', surname='Player8', tournament=self.tournament, rating=1)
        Chess_Player.objects.create(name='Player 9', surname='Player9', tournament=self.tournament, rating=1)
        self.players = Chess_Player.objects.filter(tournament=self.tournament)
        self.edit_game_url = reverse('chesstour:edit_game', args=[self.tournament.id])
    
    @mock.patch('logging.error')
    def test_edit_game_three_rounds(self, mock_log):
        self.client.login(username='testuser', password='12345')
        # Play first round
        response = self.client.post(self.edit_game_url)
        self.assertEqual(Chess_Game.objects.count(), 5)
        
        # Play second round
        response = self.client.post(self.edit_game_url)
        self.assertTrue(mock_log.call_count==1)
        self.assertEqual(Chess_Game.objects.count(), 10)
        
        #play third round
        response = self.client.post(self.edit_game_url)
        self.assertEqual(Chess_Game.objects.count(), 15)
        self.assertTrue(mock_log.call_count==3)
        
        games = Chess_Game.objects.all()
        players = Chess_Player.objects.all()
        
        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[2], players[6])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[0], players[3])))
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[4], players[5])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[7], players[8])))
        self.assertEqual(set((games[4].player1, games[4].player2)), set((players[9], players[1])))
        
        self.assertEqual(set((games[5].player1, games[5].player2)), set((players[2], players[0])))
        self.assertEqual(set((games[6].player1, games[6].player2)), set((players[6], players[4])))
        self.assertEqual(set((games[7].player1, games[7].player2)), set((players[3], players[7])))
        self.assertEqual(set((games[8].player1, games[8].player2)), set((players[5], players[9])))
        self.assertEqual(set((games[9].player1, games[9].player2)), set((players[8], players[1])))

        self.assertEqual(set((games[10].player1, games[10].player2)), set((players[2], players[3])))
        self.assertEqual(set((games[11].player1, games[11].player2)), set((players[6], players[5])))
        self.assertEqual(set((games[12].player1, games[12].player2)), set((players[0], players[8])))
        self.assertEqual(set((games[13].player1, games[13].player2)), set((players[4], players[1])))
        self.assertEqual(set((games[14].player1, games[14].player2)), set((players[9], players[7])))
    @mock.patch('logging.error')
    def test_edit_with_changing_scores(self, mock_log):
        self.client.login(username='testuser', password='12345')
        # Play first round
        response = self.client.post(self.edit_game_url)
        self.assertEqual(Chess_Game.objects.count(), 5)
        Chess_Player.objects.filter(id=3).update(rating=Chess_Player.objects.get(id=3).rating+1)
        Chess_Player.objects.filter(id=1).update(rating=Chess_Player.objects.get(id=1).rating+1)
        Chess_Player.objects.filter(id=5).update(rating=Chess_Player.objects.get(id=5).rating+1)
        Chess_Player.objects.filter(id=8).update(rating=Chess_Player.objects.get(id=8).rating+1)
        Chess_Player.objects.filter(id=10).update(rating=Chess_Player.objects.get(id=10).rating+1)
        #rating 2,0,3,1,2,1,2,2,1,2
        
        # Play second round
        response = self.client.post(self.edit_game_url)
        self.assertTrue(mock_log.call_count==0)
        self.assertEqual(Chess_Game.objects.count(), 10)
        Chess_Player.objects.filter(id=7).update(rating=Chess_Player.objects.get(id=7).rating+1)
        Chess_Player.objects.filter(id=4).update(rating=Chess_Player.objects.get(id=4).rating+1)
        Chess_Player.objects.filter(id=6).update(rating=Chess_Player.objects.get(id=6).rating+1)
        Chess_Player.objects.filter(id=9).update(rating=Chess_Player.objects.get(id=9).rating+1)
        Chess_Player.objects.filter(id=2).update(rating=Chess_Player.objects.get(id=2).rating+1)
        #rating 2,1,3,2,2,2,3,2,2,2

        #play third round
        response = self.client.post(self.edit_game_url)
        self.assertEqual(Chess_Game.objects.count(), 15)
        #self.assertEqual(mock_log.call_count,2)
        for mock_call in mock_log.call_args_list:
            with open('mock_calls.txt', 'a') as f:  # open the file in append mode
                f.write(str(mock_call) + '\n')  # write the string representation of the mock call to the file
        games = Chess_Game.objects.all()
        players = Chess_Player.objects.all()

        self.assertEqual(set((games[0].player1, games[0].player2)), set((players[2], players[6])))
        self.assertEqual(set((games[1].player1, games[1].player2)), set((players[0], players[3])))
        self.assertEqual(set((games[2].player1, games[2].player2)), set((players[4], players[5])))
        self.assertEqual(set((games[3].player1, games[3].player2)), set((players[7], players[8])))
        self.assertEqual(set((games[4].player1, games[4].player2)), set((players[9], players[1])))

        self.assertEqual(set((games[5].player1, games[5].player2)), set((players[2], players[0])))
        self.assertEqual(set((games[6].player1, games[6].player2)), set((players[4], players[6])))
        self.assertEqual(set((games[7].player1, games[7].player2)), set((players[7], players[9])))
        self.assertEqual(set((games[8].player1, games[8].player2)), set((players[3], players[5])))
        self.assertEqual(set((games[9].player1, games[9].player2)), set((players[8], players[1])))
        
        #self.assertEqual(set((games[10].player1, games[10].player2)), set((players[2], players[4])))
        #self.assertEqual(set((games[11].player1, games[11].player2)), set((players[0], players[7])))
        #self.assertEqual(set((games[12].player1, games[12].player2)), set((players[6], players[3])))
        #self.assertEqual(set((games[13].player1, games[13].player2)), set((players[5], players[8])))
        #self.assertEqual(set((games[14].player1, games[14].player2)), set((players[1], players[9])))
