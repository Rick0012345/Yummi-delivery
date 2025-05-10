from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product

def index(request):
    return render(request, 'core/index.html')

@login_required
def menu(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products})

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('nomeCategoria')
        description = request.POST.get('descricaoCategoria')
        Category.objects.create(name=name, description=description)
        return redirect('cardapio')

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('nomeProduto')
        category_id = request.POST.get('categoriaProduto')
        code = request.POST.get('codigoProduto')
        price = request.POST.get('precoProduto')
        status = request.POST.get('statusProduto')
        description = request.POST.get('descricaoProduto')
        image = request.FILES.get('imagemProduto')
        Product.objects.create(
            name=name,
            category_id=category_id,
            code=code,
            price=price,
            status=status,
            description=description,
            image=image,
        )
        return redirect('cardapio')

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('nomeCategoria')
        category.description = request.POST.get('descricaoCategoria')
        category.save()
        return redirect('cardapio')
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('cardapio')

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        name = request.POST.get('nomeProduto')
        category_id = request.POST.get('categoriaProduto')
        code = request.POST.get('codigoProduto')
        price = request.POST.get('precoProduto')
        status = request.POST.get('statusProduto')
        description = request.POST.get('descricaoProduto')
        
        if not name or not category_id or not code or price is None or not status:
            return redirect('cardapio')

        product.name = name
        product.category_id = category_id
        product.code = code
        product.price = price
        product.status = status
        product.description = description
        
        image = request.FILES.get('imagemProduto')
        if image:
            product.image = image
        
        product.save()
        return redirect('cardapio')

    return render(request, 'edit_product.html', {'product': product})

@login_required
def toggle_product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.status = 'inativo' if product.status == 'ativo' else 'ativo'
        product.save()
        return redirect('cardapio') 

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('cardapio')

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
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products, 'title': 'Cardápio', 'active': 'cardapio'})

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
