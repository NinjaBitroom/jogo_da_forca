from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TemaForm, PalavraForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def cadastrar_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.professor = request.user.professor
            tema.save()
            return redirect('index')
    else:
        form = TemaForm()
    return render(request, 'cadastrar_tema.html', {'form': form})

@login_required
def cadastrar_palavra(request):
    if request.method == 'POST':
        form = PalavraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PalavraForm()
    return render(request, 'cadastrar_palavra.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request, 'index.html')