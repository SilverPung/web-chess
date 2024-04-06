from django.shortcuts import render
from .models import Image
from .forms import LoginForm, SignupForm

def home(request):
    main_image = Image.objects.filter(name__iexact='create tournament').first()
    context = {'main_image': main_image}
    return render(request, 'core/home.html', context)

def create(request):
    return render(request, 'core/create.html')

def signup(request):
    form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})