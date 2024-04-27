from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Chess_Tournament, Chess_Player




class TournamentForm(forms.ModelForm):
    class Meta:
        model = Chess_Tournament
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300 py-2 px-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-xl bg-gray-300 py-2 px-2'}),

        }

class PlayerForm(forms.ModelForm):
    tournament = forms.ModelChoiceField(required=False,queryset=Chess_Tournament.objects.all(), widget=forms.HiddenInput())
    username = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}))
    birth_date = forms.DateField(required=False,widget=forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}))
    class Meta:
        model = Chess_Player
        fields = ['name', 'surname', 'username', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'surname': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
        }

class ScoreForm(forms.Form):
    SCORE_CHOICES = [
        (0, '0'),
        (0.5, '0.5'),
        (1, '1'),
    ]
    player1_score = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.Select(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300 text-center'}))
    player2_score = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.Select(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300 text-center'}))