from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chess_Tournament(models.Model):
    
    
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    rounds = models.IntegerField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
class Chess_Player(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    birth_date = models.DateField(null=True, blank=True)
    tournament = models.ForeignKey(Chess_Tournament, on_delete=models.CASCADE)
    white_games = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Chess_Game(models.Model):
    tournament = models.ForeignKey(Chess_Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Chess_Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Chess_Player, on_delete=models.CASCADE, related_name='player2')
    round = models.IntegerField()
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('tournament',)

    def __str__(self):
        return self.tournament.name + ' - ' + self.player1.name + ' vs ' + self.player2.name
    


