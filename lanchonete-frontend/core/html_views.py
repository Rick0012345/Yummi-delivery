from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Category, Product, Cliente, Pedido, PedidoItem, Lanchonete, UsuarioLanchonete
from .serializers import CategorySerializer, ProductSerializer, ClienteSerializer, PedidoSerializer

# Decorator para garantir que uma lanchonete está selecionada
def lanchonete_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('lanchonete_ativa'):
            messages.warning(request, 'Selecione uma lanchonete para continuar.')
            return redirect('minhas_lanchonetes')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def minhas_lanchonetes(request):
    """Lista lanchonetes do usuário e permite seleção"""
    lanchonetes = Lanchonete.objects.filter(
        Q(proprietario=request.user) |
        Q(usuariolanchonete__usuario=request.user, usuariolanchonete__ativo=True)
    ).distinct()
    
    lanchonete_ativa_id = request.session.get('lanchonete_ativa')
    lanchonete_ativa = None
    if lanchonete_ativa_id:
        try:
            lanchonete_ativa = Lanchonete.objects.get(id=lanchonete_ativa_id)
        except Lanchonete.DoesNotExist:
            request.session.pop('lanchonete_ativa', None)
            request.session.pop('lanchonete_nome', None)
    
    return render(request, 'core/lanchonetes.html', {
        'lanchonetes': lanchonetes,
        'lanchonete_ativa': lanchonete_ativa,
        'title': 'Minhas Lanchonetes',
        'active': 'lanchonetes'
    })

@login_required
def selecionar_lanchonete(request, lanchonete_id):
    """Seleciona uma lanchonete como ativa"""
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
    
    # Verifica se o usuário tem acesso a esta lanchonete
    has_access = (
        lanchonete.proprietario == request.user or
        UsuarioLanchonete.objects.filter(
            usuario=request.user, 
            lanchonete=lanchonete, 
            ativo=True
        ).exists()
    )
    
    if not has_access:
        messages.error(request, 'Você não tem permissão para acessar esta lanchonete.')
        return redirect('minhas_lanchonetes')
    
    request.session['lanchonete_ativa'] = lanchonete.id
    request.session['lanchonete_nome'] = lanchonete.nome
    messages.success(request, f'Lanchonete "{lanchonete.nome}" selecionada com sucesso!')
    return redirect('dashboard')

@login_required
def cadastrar_lanchonete(request):
    """Cadastra uma nova lanchonete"""
    if request.method == 'POST':
        try:
            lanchonete = Lanchonete.objects.create(
                nome=request.POST.get('nome'),
                cnpj=request.POST.get('cnpj'),
                telefone=request.POST.get('telefone'),
                email=request.POST.get('email'),
                endereco=request.POST.get('endereco'),
                numero=request.POST.get('numero'),
                bairro=request.POST.get('bairro'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                cep=request.POST.get('cep'),
                proprietario=request.user,
                taxa_entrega=request.POST.get('taxa_entrega', 0),
                tempo_estimado=request.POST.get('tempo_estimado', 30),
                raio_entrega=request.POST.get('raio_entrega', 5),
                dias_funcionamento=request.POST.get('dias_funcionamento', ''),
                horario_abertura=request.POST.get('horario_abertura'),
                horario_fechamento=request.POST.get('horario_fechamento'),
                dinheiro=bool(request.POST.get('dinheiro')),
                cartao_credito=bool(request.POST.get('cartao_credito')),
                cartao_debito=bool(request.POST.get('cartao_debito')),
                pix=bool(request.POST.get('pix')),
                vale_refeicao=bool(request.POST.get('vale_refeicao')),
                chave_pix=request.POST.get('chave_pix', ''),
            )
            
            if 'logo' in request.FILES:
                lanchonete.logo = request.FILES['logo']
                lanchonete.save()
            
            messages.success(request, f'Lanchonete "{lanchonete.nome}" cadastrada com sucesso!')
            return redirect('minhas_lanchonetes')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar lanchonete: {str(e)}')
    
    return render(request, 'core/cadastrar_lanchonete.html', {
        'title': 'Cadastrar Lanchonete',
        'active': 'lanchonetes'
    })

@login_required
def editar_lanchonete(request, lanchonete_id):
    """Edita uma lanchonete"""
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id, proprietario=request.user)
    
    if request.method == 'POST':
        try:
            lanchonete.nome = request.POST.get('nome')
            lanchonete.cnpj = request.POST.get('cnpj')
            lanchonete.telefone = request.POST.get('telefone')
            lanchonete.email = request.POST.get('email')
            lanchonete.endereco = request.POST.get('endereco')
            lanchonete.numero = request.POST.get('numero')
            lanchonete.bairro = request.POST.get('bairro')
            lanchonete.cidade = request.POST.get('cidade')
            lanchonete.estado = request.POST.get('estado')
            lanchonete.cep = request.POST.get('cep')
            lanchonete.taxa_entrega = request.POST.get('taxa_entrega', 0)
            lanchonete.tempo_estimado = request.POST.get('tempo_estimado', 30)
            lanchonete.raio_entrega = request.POST.get('raio_entrega', 5)
            lanchonete.dias_funcionamento = request.POST.get('dias_funcionamento', '')
            lanchonete.horario_abertura = request.POST.get('horario_abertura')
            lanchonete.horario_fechamento = request.POST.get('horario_fechamento')
            lanchonete.dinheiro = bool(request.POST.get('dinheiro'))
            lanchonete.cartao_credito = bool(request.POST.get('cartao_credito'))
            lanchonete.cartao_debito = bool(request.POST.get('cartao_debito'))
            lanchonete.pix = bool(request.POST.get('pix'))
            lanchonete.vale_refeicao = bool(request.POST.get('vale_refeicao'))
            lanchonete.chave_pix = request.POST.get('chave_pix', '')
            
            if 'logo' in request.FILES:
                lanchonete.logo = request.FILES['logo']
            
            lanchonete.save()
            messages.success(request, f'Lanchonete "{lanchonete.nome}" atualizada com sucesso!')
            return redirect('minhas_lanchonetes')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar lanchonete: {str(e)}')
    
    return render(request, 'core/editar_lanchonete.html', {
        'lanchonete': lanchonete,
        'title': 'Editar Lanchonete',
        'active': 'lanchonetes'
    })

# Helper para filtrar por lanchonete ativa
def get_lanchonete_ativa(request):
    lanchonete_id = request.session.get('lanchonete_ativa')
    if lanchonete_id:
        return get_object_or_404(Lanchonete, id=lanchonete_id)
    return None

def health_check(request):
    """Health check para o Railway"""
    return JsonResponse({'status': 'ok', 'message': 'Django app is running'})

def index(request):
    """Página inicial - redireciona para login se não autenticado"""
    if request.user.is_authenticated:
        if not request.session.get('lanchonete_ativa'):
            return redirect('minhas_lanchonetes')
        return render(request, 'core/index.html')
    else:
        return redirect('login')

@login_required
@lanchonete_required
def menu(request):
    lanchonete = get_lanchonete_ativa(request)
    categories = Category.objects.filter(lanchonete=lanchonete)
    products = Product.objects.filter(lanchonete=lanchonete)
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products})

@login_required
@lanchonete_required
def add_category(request):
    if request.method == 'POST':
        lanchonete = get_lanchonete_ativa(request)
        name = request.POST.get('nomeCategoria')
        description = request.POST.get('descricaoCategoria')
        Category.objects.create(name=name, description=description, lanchonete=lanchonete)
        return redirect('cardapio')

@login_required
@lanchonete_required
def add_product(request):
    if request.method == 'POST':
        lanchonete = get_lanchonete_ativa(request)
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
            lanchonete=lanchonete,
        )
        return redirect('cardapio')

@login_required
@lanchonete_required
def edit_category(request, category_id):
    lanchonete = get_lanchonete_ativa(request)
    category = get_object_or_404(Category, id=category_id, lanchonete=lanchonete)
    if request.method == 'POST':
        category.name = request.POST.get('nomeCategoria')
        category.description = request.POST.get('descricaoCategoria')
        category.save()
        return redirect('cardapio')

@login_required
@lanchonete_required
def delete_category(request, category_id):
    lanchonete = get_lanchonete_ativa(request)
    category = get_object_or_404(Category, id=category_id, lanchonete=lanchonete)
    if request.method == 'POST':
        category.delete()
        return redirect('cardapio')

@login_required
@lanchonete_required
def edit_product(request, product_id):
    lanchonete = get_lanchonete_ativa(request)
    product = get_object_or_404(Product, id=product_id, lanchonete=lanchonete)
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
@lanchonete_required
def toggle_product_status(request, product_id):
    lanchonete = get_lanchonete_ativa(request)
    product = get_object_or_404(Product, id=product_id, lanchonete=lanchonete)
    if request.method == 'POST':
        product.status = 'inativo' if product.status == 'ativo' else 'ativo'
        product.save()
        return redirect('cardapio')

@login_required
@lanchonete_required
def delete_product(request, product_id):
    lanchonete = get_lanchonete_ativa(request)
    product = get_object_or_404(Product, id=product_id, lanchonete=lanchonete)
    if request.method == 'POST':
        product.delete()
        return redirect('cardapio')

@login_required
@lanchonete_required
def dashboard(request):
    lanchonete = get_lanchonete_ativa(request)
    context = {
        'title': 'Dashboard',
        'active': 'dashboard',
        'lanchonete': lanchonete,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
@lanchonete_required
def pedidos(request):
    lanchonete = get_lanchonete_ativa(request)
    if request.method == 'POST':
        # Create new Pedido and its items
        cliente_id = request.POST.get('cliente')
        tipo_entrega = request.POST.get('tipoEntrega')
        observacao = request.POST.get('observacaoPedido', '')
        status = 'pendente'
        taxa_entrega = 0
        total = 0
        cliente = get_object_or_404(Cliente, id=cliente_id, lanchonete=lanchonete)
        pedido = Pedido.objects.create(
            lanchonete=lanchonete,
            cliente=cliente,
            tipo_entrega=tipo_entrega,
            status=status,
            observacao=observacao,
            taxa_entrega=taxa_entrega,
            total=0,
        )
        # Handle items
        produtos = request.POST.getlist('produto[]')
        quantidades = request.POST.getlist('quantidade[]')
        observacoes = request.POST.getlist('observacao[]')
        for i, produto_id in enumerate(produtos):
            produto = get_object_or_404(Product, id=produto_id, lanchonete=lanchonete)
            quantidade = int(quantidades[i])
            obs = observacoes[i] if i < len(observacoes) else ''
            valor_unitario = produto.price
            PedidoItem.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                observacao=obs,
            )
            total += valor_unitario * quantidade
        pedido.total = total
        pedido.save()
        return redirect('pedidos')
    pedidos = Pedido.objects.filter(lanchonete=lanchonete).select_related('cliente').prefetch_related('itens__produto').all().order_by('-data_hora')
    clientes = Cliente.objects.filter(lanchonete=lanchonete)
    produtos = Product.objects.filter(lanchonete=lanchonete)
    return render(request, 'core/pedidos.html', {
        'pedidos': pedidos,
        'clientes': clientes,
        'produtos': produtos,
        'title': 'Pedidos',
        'active': 'pedidos',
    })

@login_required
@lanchonete_required
def cardapio(request):
    lanchonete = get_lanchonete_ativa(request)
    categories = Category.objects.filter(lanchonete=lanchonete)
    products = Product.objects.filter(lanchonete=lanchonete)
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products, 'title': 'Cardápio', 'active': 'cardapio'})

@login_required
@lanchonete_required
def clientes(request):
    lanchonete = get_lanchonete_ativa(request)
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            # Delete Cliente
            cliente = get_object_or_404(Cliente, id=request.POST.get('delete_id'), lanchonete=lanchonete)
            cliente.delete()
            return redirect('clientes')
        elif 'edit_id' in request.POST:
            # Edit Cliente
            cliente = get_object_or_404(Cliente, id=request.POST.get('edit_id'), lanchonete=lanchonete)
            data = request.POST.copy()
            data['lanchonete'] = lanchonete.id
            serializer = ClienteSerializer(cliente, data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect('clientes')
            # If invalid, fall through to render with errors
        else:
            # New Cliente
            data = request.POST.copy()
            data['lanchonete'] = lanchonete.id
            serializer = ClienteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect('clientes')
    else:
        serializer = ClienteSerializer()
    clientes = Cliente.objects.filter(lanchonete=lanchonete)
    return render(request, 'core/clientes.html', {
        'clientes': clientes,
        'serializer': serializer,
    })

@login_required
@lanchonete_required
def cozinha(request):
    lanchonete = get_lanchonete_ativa(request)
    context = {
        'title': 'Cozinha',
        'active': 'cozinha',
        'lanchonete': lanchonete,
    }
    return render(request, 'core/cozinha.html', context)

@login_required
@lanchonete_required
def configuracoes(request):
    lanchonete = get_lanchonete_ativa(request)
    if request.method == 'POST':
        # Atualizar configurações da lanchonete
        try:
            lanchonete.nome = request.POST.get('nome_lanchonete', lanchonete.nome)
            lanchonete.telefone = request.POST.get('telefone', lanchonete.telefone)
            lanchonete.email = request.POST.get('email', lanchonete.email)
            lanchonete.endereco = request.POST.get('endereco', lanchonete.endereco)
            lanchonete.taxa_entrega = request.POST.get('taxa_entrega', lanchonete.taxa_entrega)
            lanchonete.tempo_estimado = request.POST.get('tempo_estimado', lanchonete.tempo_estimado)
            lanchonete.save()
            messages.success(request, 'Configurações atualizadas com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar configurações: {str(e)}')
        return redirect('configuracoes')
    
    context = {
        'title': 'Configurações',
        'active': 'configuracoes',
        'lanchonete': lanchonete,
    }
    return render(request, 'core/configuracoes.html', context)
