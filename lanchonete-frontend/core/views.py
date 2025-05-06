from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'core/index.html')

@login_required
def dashboard(request):
    context = {
        'title': 'Dashboard',
        'active': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def pedidos(request):
    context = {
        'title': 'Pedidos',
        'active': 'pedidos',
    }
    return render(request, 'core/pedidos.html', context)

@login_required
def cardapio(request):
    context = {
        'title': 'Cardápio',
        'active': 'cardapio',
    }
    return render(request, 'core/cardapio.html', context)

@login_required
def clientes(request):
    context = {
        'title': 'Clientes',
        'active': 'clientes',
    }
    return render(request, 'core/clientes.html', context)

@login_required
def cozinha(request):
    context = {
        'title': 'Cozinha',
        'active': 'cozinha',
    }
    return render(request, 'core/cozinha.html', context)

@login_required
def configuracoes(request):
    context = {
        'title': 'Configurações',
        'active': 'configuracoes',
    }
    return render(request, 'core/configuracoes.html', context)
