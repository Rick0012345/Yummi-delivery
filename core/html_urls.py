from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import html_views

# HTML/template views URLs (optional)
urlpatterns = [
    path('', html_views.index, name='index'),
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
]