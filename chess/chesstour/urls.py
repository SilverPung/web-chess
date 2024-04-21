from django.urls import path
from . import views

app_name = 'chesstour'
urlpatterns = [
    path('create/', views.create_new, name='create_new'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('game/<int:pk>', views.game, name='game'),
]