from django.shortcuts import get_object_or_404, redirect, render
from .models import Cliente, Atendente, Departamento, Situacao
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def abrir_index(request):
    usuario_logado = request.user.username
    return render(request, 'index.html', {'usuario_logado': usuario_logado})


def cad_cliente(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_cliente.html', {'usuario_logado': usuario_logado})

def login(request):
    usuario_logado = request.user.username
    return render(request, 'login.html', {'usuario_logado': usuario_logado})


def salva_cliente_novo(request):
    usuario_logado = request.user.username
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')

        grava_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            email=email,
            observacao=observacao
        )

        grava_cliente.save()
        messages.info(request, 'Cliente ' + nome + ' cadastrado com sucesso')
        return render(request, 'Cad_cliente.html', {'usuario_logado': usuario_logado})

@login_required
def cons_cliente(request):
    usuario_logado = request.user.username
    dado_pesquisa_nome = request.POST.get('cliente')
    dado_pesquisa_telefone = request.POST.get('telefone')
    dado_pesquisa_email = request.POST.get('email')
    
    page = request.GET.get('page')
    
    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa)
        paginator = Paginator(clientes, 5)
     
        cliente = paginator.get_page(page)
            
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': cliente, 'dado_pesquisa': dado_pesquisa})
        
    if dado_pesquisa_nome is not None and dado_pesquisa_nome != '':
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        
        paginator = Paginator(clientes, 5)
        
        page = request.GET.get('page')
     
        cliente = paginator.get_page(page)
            
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': cliente, 'dado_pesquisa': dado_pesquisa_nome})
    
    
    elif dado_pesquisa_telefone is not None and dado_pesquisa_telefone != '':
        clientes = Cliente.objects.filter(telefone__icontains=dado_pesquisa_telefone)
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': clientes})
    
    elif dado_pesquisa_email is not None and dado_pesquisa_email != '':
        clientes = Cliente.objects.filter(email__icontains=dado_pesquisa_email)
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': clientes})
    
    else:
        return render(request, 'Cons_Cliente_Lista.html', {'usuario_logado': usuario_logado})

@login_required
def edit_cliente(request, id):
    usuario_logado = request.user.username
    dados_editar = get_object_or_404(Cliente, pk=id)
    return render(request, 'Edit_Cliente.html', {'usuario_logado': usuario_logado, 'dados_do_cliente': dados_editar})

def salvar_cliente_editado(request):
        usuario_logado = request.user.username
        if request.method == 'POST':
            
            id_cliente  = request.POST.get('id_cliente')
            nome = request.POST.get('nome')
            telefone = request.POST.get('telefone')
            email = request.POST.get('email')
            observacao = request.POST.get('observacao')
            
            Cliente_Editado = Cliente.objects.get(id=id_cliente)
            
            Cliente_Editado.nome = nome
            Cliente_Editado.telefone = telefone
            Cliente_Editado.email = email
            Cliente_Editado.observacao = observacao
            
            Cliente_Editado.save()
        
            messages.info(request, 'Cliente ' + nome  +' editado com sucesso')
            return render(request, 'Cons_Cliente_Lista.html', {'usuario_logado': usuario_logado})
        
        
@login_required
def delete_cliente(request, id):
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()
    
    messages.info(request, 'Cliente ' + nome + ' excluido com sucesso')
    return redirect(cons_cliente)


@login_required
def salvar_atend_novo(request):
    usuario_logado = request.user.username
    
    if (request.method == 'POST'):
        nome_atend = request.POST.get('nome_atend')
        telefone_atend = request.POST.get('telefone_atend')
        user_atend = request.POST.get('user_atend')
        observacao_atend = request.POST.get('observacao_atend')
        
        if user_atend:
            user_atend = User.objects.get(username=user_atend)
        else:
            user_atend = None
        
        grava_atend = Atendente(
            nome_atend=nome_atend,
            telefone_atend=telefone_atend,
            observacao_atend=observacao_atend,
            ativo_atend=1,
            user_atend=user_atend
        )
        
        grava_atend.save()
        messages.info(request, 'Atendente ' + nome_atend + ' cadastrado com sucesso!', 'cad_atend')
        cons_users = User.objects.all()
        return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})

@login_required
def edit_atend(request, id):
    usuario_logado = request.user.username
    cons_users = User.objects.all()
    dados_logar = get_object_or_404(Atendente, pk=id)
    return render(request, 'Edit_Atendente.html', {'dados_do_atendente': dados_logar, 'usuario_logado': usuario_logado, 'cons_users': cons_users})
    
    
@login_required
def cad_atend(request):
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    
    return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})

@login_required
def cons_atend(request):
    dado_pesquisa_atendente = request.POST.get('atendente')
    dado_pesquisa_todos = request.POST.get('seleciona_todos')
    
    usuario_logado = request.user.username
    
    if dado_pesquisa_todos == 'N' and dado_pesquisa_atendente != None:
        todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)
    
    elif dado_pesquisa_todos == 'S' and dado_pesquisa_atendente != None:
        todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente, ativo_atend=1)
    
    elif dado_pesquisa_todos == 'N' and dado_pesquisa_atendente == None:
        todos_atendentes = Atendente.objects.all()
        
    else:
        todos_atendentes = Atendente.objects.filter(ativo_atend=1)
    
    page = request.GET.get('page')
    
    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        atendentes_lista = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa)
        paginas = Paginator(atendentes_lista, 3)
        page = request.GET.get(page)
        atendentes = paginas.get_page(page)
        
        return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})
    
    if dado_pesquisa_atendente != None and dado_pesquisa_atendente != '':
        atendentes_lista = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)
        paginas = Paginator(atendentes_lista, 3)
        page = request.GET.get(page)
        atendentes = paginas.get_page(page)
        
        return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente, 'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Atendente.html', {'todos_atendentes': todos_atendentes, 'usuario_logado': usuario_logado})
    
    
@login_required
def salvar_atend_editado(request):
        usuario_logado = request.user.username
        if request.method == 'POST':
            
            id_atendente  = request.POST.get('id_atendente')
            nome_atend = request.POST.get('nome_atend')
            telefone_atend = request.POST.get('telefone_atend')
            observacao_atend = request.POST.get('observacao_atend')
            user_atend =  request.POST.get('user_atend')
            
            user_atend = User.objects.get(username=user_atend)
            Atend_Editado = Atendente.objects.get(id=id_atendente)
            
            Atend_Editado.nome_atend = nome_atend
            Atend_Editado.telefone_atend = telefone_atend
            Atend_Editado.observacao_atend = observacao_atend
            Atend_Editado.user_atende = user_atend
            
            Atend_Editado.save()
        
            messages.info(request, 'Atendente ' + nome_atend  +' editado com sucesso')
            return render(request, 'Cons_Atendente.html', {'usuario_logado': usuario_logado})


@login_required
def cad_depto(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})


@login_required
def salvar_depto_novo(request):
    usuario_logado = request.user.username
    
    if (request.method == 'POST'):
        nome_depto = request.POST.get('nome_depto')
        observacao_depto = request.POST.get('observacao_depto')
        
        grava_depto = Departamento(
            nome_depto=nome_depto,
            observacao_depto=observacao_depto,
            ativo_depto=1
        )
        
        grava_depto.save()
        messages.info(request, 'Departamento ' + nome_depto + ' cadastrado com sucesso!', 'cad_depto')
        return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})


@login_required
def cons_depto(request):
    dado_pesquisa_depto = request.POST.get('departamento')
    usuario_logado = request.user.username
    todos_deptos = Departamento.objects.all()
    page = request.GET.get('page')
    
    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        depto_lista = Departamento.objects.filter(nome_depto__icontains=dado_pesquisa)
        
        paginas = Paginator(depto_lista, 5)
        page = request.GET.get(page)
        departamentos = paginas.get_page(page)
        
        return render(request, 'Cons_Depto.html', {'todos_deptos': departamentos, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})
    
    if dado_pesquisa_depto != None and dado_pesquisa_depto != '':
        depto_lista = Departamento.objects.filter(nome_depto__icontains=dado_pesquisa_depto)
        
        paginas = Paginator(depto_lista, 5)
        page = request.GET.get(page)
        departamentos = paginas.get_page(page)
        
        return render(request, 'Cons_Depto.html', {'todos_deptos': departamentos, 'dado_pesquisa': dado_pesquisa_depto, 'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Depto.html', {'todos_deptos': todos_deptos, 'usuario_logado': usuario_logado})


@login_required
def edit_depto(request, id):
    usuario_logado = request.user.username
    dados_editar = get_object_or_404(Departamento, pk=id)
    return render(request, 'Edit_Depto.html', {'usuario_logado': usuario_logado, 'dados_do_depto': dados_editar})

def salvar_depto_editado(request):
        usuario_logado = request.user.username
        if request.method == 'POST':
            
            id_departamento  = request.POST.get('id_departamento')
            nome_depto = request.POST.get('nome_depto')
            observacao_depto = request.POST.get('observacao_depto')
            
            Depto_Editado = Departamento.objects.get(id=id_departamento)
            
            Depto_Editado.nome_depto = nome_depto
            Depto_Editado.observacao_depto = observacao_depto   
            
            Depto_Editado.save()
        
            messages.info(request, 'Departamento ' + nome_depto  +' editado com sucesso')
            return render(request, 'Cons_Depto.html', {'usuario_logado': usuario_logado})
        

@login_required
def cad_situacao(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_situacao_novo(request):
    usuario_logado = request.user.username
    
    if (request.method == 'POST'):
        descricao_situacao = request.POST.get('descricao_situacao')
        info_situacao = request.POST.get('info_situacao')
        
        grava_situacao = Situacao(
            descricao_situacao=descricao_situacao,
            info_situacao=info_situacao,
            ativo_situacao=1
        )
        
        grava_situacao.save()
        messages.info(request, 'Situacao ' + descricao_situacao + ' cadastrado com sucesso!', 'cad_situacao')
        return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})


@login_required
def cons_situacao(request):
    dado_pesquisa_situacao = request.POST.get('situacao')
    usuario_logado = request.user.username
    todas_situacao = Situacao.objects.all()
    page = request.GET.get('page')
    print(todas_situacao)
    
    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        situacao_lista = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa)
        
        paginas = Paginator(situacao_lista, 5)
        page = request.GET.get(page)
        situacao = paginas.get_page(page)
        
        return render(request, 'Cons_Situacao.html', {'todas_situacao': situacao, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})
    
    if dado_pesquisa_situacao != None and dado_pesquisa_situacao != '':
        situacao_lista = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa_situacao)
        
        paginas = Paginator(situacao_lista, 5)
        page = request.GET.get(page)
        situacao = paginas.get_page(page)
        
        return render(request, 'Cons_Situacao.html', {'todas_situacao': situacao, 'dado_pesquisa': dado_pesquisa_situacao, 'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Situacao.html', {'todas_situacao': todas_situacao, 'usuario_logado': usuario_logado})


@login_required
def edit_situacao(request, id):
    usuario_logado = request.user.username
    dados_editar = get_object_or_404(Situacao, pk=id)
    return render(request, 'Edit_Situacao.html', {'usuario_logado': usuario_logado, 'dados_da_situacao': dados_editar})

def salvar_situacao_editado(request):
        usuario_logado = request.user.username
        if request.method == 'POST':
            
            id_situacao  = request.POST.get('id_situacao')
            descricao_situacao = request.POST.get('descricao_situacao')
            info_situacao = request.POST.get('info_situacao')
            
            Situacao_Editado = Situacao.objects.get(id=id_situacao)
            
            Situacao_Editado.descricao_situacao = descricao_situacao
            Situacao_Editado.info_situacao = info_situacao   
            
            Situacao_Editado.save()
        
            messages.info(request, 'Situação ' + descricao_situacao  +' editado com sucesso')
            return render(request, 'Cons_Situacao.html', {'usuario_logado': usuario_logado})