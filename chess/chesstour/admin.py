from django.contrib import admin

# Register your models here.
from .models import Chess_Tournament, Chess_Player, Chess_Game

admin.site.register(Chess_Tournament)
admin.site.register(Chess_Player)
admin.site.register(Chess_Game)