from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('clientes/', views.clientes, name='clientes'),
    path('cozinha/', views.cozinha, name='cozinha'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
