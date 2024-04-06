from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Chess_Tournament, Chess_Player




class TournamentForm(forms.ModelForm):
    class Meta:
        model = Chess_Tournament
        fields = ['name', 'description', 'rounds']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-xl bg-gray-300'}),
            'rounds': forms.NumberInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Chess_Player
        fields = ['name', 'surname', 'username', 'rating', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'surname': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'username': forms.TextInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300'}),
        }