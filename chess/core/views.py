from django.shortcuts import render, redirect
from .models import Image
from .forms import LoginForm, SignupForm
from django.contrib.auth import logout

def home(request):
    main_image = Image.objects.filter(name__iexact='create tournament').first()
    context = {'main_image': main_image}
    return render(request, 'core/home.html', context)

def create(request):
    return render(request, 'core/create.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def logout_view(request):#funkcja odpowiadająca za wylogowanie
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'core/logout.html')#wyświetlenie strony wylogowania