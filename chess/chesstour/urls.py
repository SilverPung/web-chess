from django.urls import path
from . import views

app_name = 'chesstour'
urlpatterns = [
    path('create/', views.create_new, name='create_new'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('game/<int:pk>', views.game, name='game'),
    path('edit_game/<int:pk>', views.edit_game, name='edit_game'),
    path('players/<int:pk>/<int:spk>/', views.manage_players, name='manage_players'),
    path('view_results/<int:pk>/', views.view_results, name='view_results')
]