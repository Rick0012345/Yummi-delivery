from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Cliente, Pedido, PedidoItem, Lanchonete
from .serializers import CategorySerializer, ProductSerializer, ClienteSerializer, PedidoSerializer

@login_required
def index(request):
    # Verificar se há lanchonete selecionada na sessão
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    return redirect('dashboard')

@login_required
def selecionar_lanchonete(request):
    if request.method == 'POST':
        lanchonete_id = request.POST.get('lanchonete_id')
        if lanchonete_id:
            try:
                lanchonete = Lanchonete.objects.get(id=lanchonete_id, status='ativa')
                request.session['lanchonete_id'] = lanchonete.id
                request.session['lanchonete_nome'] = lanchonete.nome
                messages.success(request, f'Lanchonete "{lanchonete.nome}" selecionada com sucesso!')
                return redirect('dashboard')
            except Lanchonete.DoesNotExist:
                messages.error(request, 'Lanchonete não encontrada ou inativa.')
    
    lanchonetes = Lanchonete.objects.filter(status='ativa').order_by('nome')
    context = {
        'title': 'Selecionar Lanchonete',
        'lanchonetes': lanchonetes,
    }
    return render(request, 'core/selecionar_lanchonete.html', context)

@login_required
def trocar_lanchonete(request):
    if 'lanchonete_id' in request.session:
        del request.session['lanchonete_id']
        del request.session['lanchonete_nome']
    return redirect('selecionar_lanchonete')

@login_required
def menu(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products})

@login_required
def add_category(request):
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
    if request.method == 'POST':
        name = request.POST.get('nomeCategoria')
        description = request.POST.get('descricaoCategoria')
        Category.objects.create(
            name=name, 
            description=description,
            lanchonete_id=request.session['lanchonete_id']
        )
        return redirect('cardapio')

@login_required
def add_product(request):
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
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
            lanchonete_id=request.session['lanchonete_id'],
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
    # Verificar se há lanchonete selecionada
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
    try:
        lanchonete = Lanchonete.objects.get(id=request.session['lanchonete_id'])
    except Lanchonete.DoesNotExist:
        del request.session['lanchonete_id']
        del request.session['lanchonete_nome']
        return redirect('selecionar_lanchonete')
    
    # Estatísticas da lanchonete selecionada
    total_pedidos = lanchonete.pedidos.count()
    total_clientes = lanchonete.clientes.filter(status='ativo').count()
    total_produtos = lanchonete.produtos.filter(status='ativo').count()
    total_categorias = lanchonete.categorias.count()
    
    context = {
        'title': 'Dashboard',
        'active': 'dashboard',
        'lanchonete': lanchonete,
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def pedidos(request):
    if request.method == 'POST':
        # Create new Pedido and its items
        cliente_id = request.POST.get('cliente')
        tipo_entrega = request.POST.get('tipoEntrega')
        observacao = request.POST.get('observacaoPedido', '')
        status = 'pendente'
        taxa_entrega = 0
        total = 0
        cliente = get_object_or_404(Cliente, id=cliente_id)
        pedido = Pedido.objects.create(
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
            produto = get_object_or_404(Product, id=produto_id)
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
    pedidos = Pedido.objects.select_related('cliente').prefetch_related('itens__produto').all().order_by('-data_hora')
    clientes = Cliente.objects.all()
    produtos = Product.objects.all()
    return render(request, 'core/pedidos.html', {
        'pedidos': pedidos,
        'clientes': clientes,
        'produtos': produtos,
        'title': 'Pedidos',
        'active': 'pedidos',
    })

@login_required
def cardapio(request):
    # Verificar se há lanchonete selecionada
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
    lanchonete_id = request.session['lanchonete_id']
    categories = Category.objects.filter(lanchonete_id=lanchonete_id)
    products = Product.objects.filter(lanchonete_id=lanchonete_id)
    return render(request, 'core/cardapio.html', {'categories': categories, 'products': products, 'title': 'Cardápio', 'active': 'cardapio'})

@login_required
def clientes(request):
    # Verificar se há lanchonete selecionada
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
    lanchonete_id = request.session['lanchonete_id']
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            # Delete Cliente
            cliente = get_object_or_404(Cliente, id=request.POST.get('delete_id'))
            cliente.delete()
            return redirect('clientes')
        elif 'edit_id' in request.POST:
            # Edit Cliente
            cliente = get_object_or_404(Cliente, id=request.POST.get('edit_id'))
            serializer = ClienteSerializer(cliente, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('clientes')
            # If invalid, fall through to render with errors
        else:
            # New Cliente
            data = request.POST.copy()
            data['lanchonete'] = lanchonete_id
            serializer = ClienteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect('clientes')
    else:
        serializer = ClienteSerializer()
    clientes = Cliente.objects.filter(lanchonete_id=lanchonete_id)
    return render(request, 'core/clientes.html', {
        'clientes': clientes,
        'serializer': serializer,
        'title': 'Clientes',
        'active': 'clientes',
    })

@login_required
def cozinha(request):
    context = {
        'title': 'Cozinha',
        'active': 'cozinha',
    }
    return render(request, 'core/cozinha.html', context)

@login_required
def configuracoes(request):
    # Verificar se há lanchonete selecionada
    if 'lanchonete_id' not in request.session:
        return redirect('selecionar_lanchonete')
    
    try:
        lanchonete = Lanchonete.objects.get(id=request.session['lanchonete_id'])
    except Lanchonete.DoesNotExist:
        del request.session['lanchonete_id']
        del request.session['lanchonete_nome']
        return redirect('selecionar_lanchonete')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'informacoes':
            # Atualizar informações da lanchonete
            lanchonete.nome = request.POST.get('nome')
            lanchonete.cnpj = request.POST.get('cnpj')
            lanchonete.telefone = request.POST.get('telefone')
            lanchonete.email = request.POST.get('email')
            lanchonete.endereco = request.POST.get('endereco')
            lanchonete.numero = request.POST.get('numero', 'S/N')
            lanchonete.bairro = request.POST.get('bairro')
            lanchonete.cidade = request.POST.get('cidade')
            lanchonete.estado = request.POST.get('estado')
            lanchonete.cep = request.POST.get('cep')
            
            # Logo (apenas se uma nova for enviada)
            if request.FILES.get('logo'):
                lanchonete.logo = request.FILES.get('logo')
            
            try:
                lanchonete.save()
                messages.success(request, 'Informações atualizadas com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar informações: {str(e)}')
        
        elif form_type == 'entrega':
            # Atualizar configurações de entrega
            lanchonete.taxa_entrega = request.POST.get('taxa_entrega', 0)
            lanchonete.tempo_estimado = request.POST.get('tempo_estimado', 30)
            lanchonete.raio_entrega = request.POST.get('raio_entrega', 5)
            
            # Dias de funcionamento
            dias_selecionados = []
            dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
            for dia in dias_semana:
                if request.POST.get(dia):
                    dias_selecionados.append(dia)
            lanchonete.dias_funcionamento = ','.join(dias_selecionados)
            
            # Horários
            horario_abertura = request.POST.get('horario_abertura')
            horario_fechamento = request.POST.get('horario_fechamento')
            lanchonete.horario_abertura = horario_abertura if horario_abertura else None
            lanchonete.horario_fechamento = horario_fechamento if horario_fechamento else None
            
            try:
                lanchonete.save()
                messages.success(request, 'Configurações de entrega atualizadas com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar configurações: {str(e)}')
        
        elif form_type == 'pagamento':
            # Atualizar formas de pagamento
            lanchonete.pix = request.POST.get('pix') == 'on'
            lanchonete.chave_pix = request.POST.get('chave_pix', '')
            
            try:
                lanchonete.save()
                messages.success(request, 'Formas de pagamento atualizadas com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar formas de pagamento: {str(e)}')
        
        return redirect('configuracoes')
    
    # Processar dias de funcionamento para exibição
    dias_funcionamento = []
    if lanchonete.dias_funcionamento:
        dias_funcionamento = lanchonete.dias_funcionamento.split(',')
    
    context = {
        'title': 'Configurações',
        'active': 'configuracoes',
        'lanchonete': lanchonete,
        'dias_funcionamento': dias_funcionamento,
    }
    return render(request, 'core/configuracoes.html', context)

# Views para gerenciar lanchonetes
@login_required
def lanchonetes(request):
    lanchonetes = Lanchonete.objects.all().order_by('nome')
    context = {
        'title': 'Lanchonetes',
        'active': 'lanchonetes',
        'lanchonetes': lanchonetes,
    }
    return render(request, 'core/lanchonetes.html', context)

@login_required
def add_lanchonete(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')
        numero = request.POST.get('numero', 'S/N')
        bairro = request.POST.get('bairro', 'Centro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado', 'RJ')
        cep = request.POST.get('cep')
        taxa_entrega = request.POST.get('taxa_entrega', 0)
        tempo_estimado = request.POST.get('tempo_estimado', 30)
        raio_entrega = request.POST.get('raio_entrega', 5)
        dias_funcionamento = request.POST.get('dias_funcionamento')
        horario_abertura = request.POST.get('horario_abertura')
        horario_fechamento = request.POST.get('horario_fechamento')
        chave_pix = request.POST.get('chave_pix')
        logo = request.FILES.get('logo')
        
        # Opções de pagamento
        pix = request.POST.get('pix') == 'on'
        
        try:
            Lanchonete.objects.create(
                nome=nome,
                cnpj=cnpj,
                telefone=telefone,
                email=email,
                endereco=endereco,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep,
                taxa_entrega=taxa_entrega,
                tempo_estimado=tempo_estimado,
                raio_entrega=raio_entrega,
                dias_funcionamento=dias_funcionamento,
                horario_abertura=horario_abertura if horario_abertura else None,
                horario_fechamento=horario_fechamento if horario_fechamento else None,
                chave_pix=chave_pix,
                logo=logo,
                pix=pix,
            )
            messages.success(request, f'Lanchonete "{nome}" cadastrada com sucesso!')
            # Se veio da tela de seleção, redireciona para lá
            if request.GET.get('from') == 'selecionar':
                return redirect('selecionar_lanchonete')
            return redirect('lanchonetes')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar lanchonete: {str(e)}')
    
    return redirect('lanchonetes')

@login_required
def edit_lanchonete(request, lanchonete_id):
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
    
    if request.method == 'POST':
        lanchonete.nome = request.POST.get('nome')
        lanchonete.cnpj = request.POST.get('cnpj')
        lanchonete.telefone = request.POST.get('telefone')
        lanchonete.email = request.POST.get('email')
        lanchonete.endereco = request.POST.get('endereco')
        lanchonete.numero = request.POST.get('numero', 'S/N')
        lanchonete.bairro = request.POST.get('bairro', 'Centro')
        lanchonete.cidade = request.POST.get('cidade')
        lanchonete.estado = request.POST.get('estado', 'RJ')
        lanchonete.cep = request.POST.get('cep')
        lanchonete.taxa_entrega = request.POST.get('taxa_entrega', 0)
        lanchonete.tempo_estimado = request.POST.get('tempo_estimado', 30)
        lanchonete.raio_entrega = request.POST.get('raio_entrega', 5)
        lanchonete.dias_funcionamento = request.POST.get('dias_funcionamento')
        lanchonete.horario_abertura = request.POST.get('horario_abertura') if request.POST.get('horario_abertura') else None
        lanchonete.horario_fechamento = request.POST.get('horario_fechamento') if request.POST.get('horario_fechamento') else None
        lanchonete.chave_pix = request.POST.get('chave_pix')
        
        # Opções de pagamento
        lanchonete.pix = request.POST.get('pix') == 'on'
        
        # Logo (apenas se uma nova for enviada)
        if request.FILES.get('logo'):
            lanchonete.logo = request.FILES.get('logo')
        
        try:
            lanchonete.save()
            messages.success(request, 'Lanchonete atualizada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar lanchonete: {str(e)}')
    
    return redirect('lanchonetes')

@login_required
def toggle_lanchonete_status(request, lanchonete_id):
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
    lanchonete.status = 'inativa' if lanchonete.status == 'ativa' else 'ativa'
    lanchonete.save()
    
    status_text = 'ativada' if lanchonete.status == 'ativa' else 'desativada'
    messages.success(request, f'Lanchonete {status_text} com sucesso!')
    return redirect('lanchonetes')

@login_required
def delete_lanchonete(request, lanchonete_id):
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
    nome = lanchonete.nome
    lanchonete.delete()
    messages.success(request, f'Lanchonete "{nome}" excluída com sucesso!')
    return redirect('lanchonetes')

@login_required
def view_lanchonete(request, lanchonete_id):
    lanchonete = get_object_or_404(Lanchonete, id=lanchonete_id)
    
    # Estatísticas da lanchonete
    total_clientes = lanchonete.clientes.filter(status='ativo').count()
    total_produtos = lanchonete.produtos.filter(status='ativo').count()
    total_categorias = lanchonete.categorias.count()
    total_pedidos = lanchonete.pedidos.count()
    
    context = {
        'title': f'Lanchonete - {lanchonete.nome}',
        'active': 'lanchonetes',
        'lanchonete': lanchonete,
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_pedidos': total_pedidos,
    }
    return render(request, 'core/view_lanchonete.html', context)
