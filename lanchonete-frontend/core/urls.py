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
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('toggle_product_status/<int:product_id>/', views.toggle_product_status, name='toggle_product_status'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]
