from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import html_views

# HTML/template views URLs (optional)
urlpatterns = [
    path('', html_views.index, name='index'),
    path('selecionar-lanchonete/', html_views.selecionar_lanchonete, name='selecionar_lanchonete'),
    path('trocar-lanchonete/', html_views.trocar_lanchonete, name='trocar_lanchonete'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', html_views.dashboard, name='dashboard'),
    path('pedidos/', html_views.pedidos, name='pedidos'),
    path('cardapio/', html_views.cardapio, name='cardapio'),
    path('clientes/', html_views.clientes, name='clientes'),
    path('cozinha/', html_views.cozinha, name='cozinha'),
    path('configuracoes/', html_views.configuracoes, name='configuracoes'),
    path('add_category/', html_views.add_category, name='add_category'),
    path('add_product/', html_views.add_product, name='add_product'),
    path('edit_category/<int:category_id>/', html_views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', html_views.delete_category, name='delete_category'),
    path('edit_product/<int:product_id>/', html_views.edit_product, name='edit_product'),
    path('toggle_product_status/<int:product_id>/', html_views.toggle_product_status, name='toggle_product_status'),
    path('delete_product/<int:product_id>/', html_views.delete_product, name='delete_product'),
    
    # URLs para lanchonetes
    path('lanchonetes/', html_views.lanchonetes, name='lanchonetes'),
    path('add_lanchonete/', html_views.add_lanchonete, name='add_lanchonete'),
    path('edit_lanchonete/<int:lanchonete_id>/', html_views.edit_lanchonete, name='edit_lanchonete'),
    path('toggle_lanchonete_status/<int:lanchonete_id>/', html_views.toggle_lanchonete_status, name='toggle_lanchonete_status'),
    path('delete_lanchonete/<int:lanchonete_id>/', html_views.delete_lanchonete, name='delete_lanchonete'),
    path('view_lanchonete/<int:lanchonete_id>/', html_views.view_lanchonete, name='view_lanchonete'),
]