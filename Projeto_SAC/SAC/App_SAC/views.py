from django.shortcuts import get_object_or_404, redirect, render
from .models import Cliente, Atendente, Departamento, Situacao, Atendimento, Situacao_Atendimento
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

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
            
            print(id_cliente)
            
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
        
        return render(request, 'Cons_Atendente_Lista.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente, 'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Atendente_Lista.html', {'todos_atendentes': todos_atendentes, 'usuario_logado': usuario_logado})
    
    
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
            return render(request, 'Cons_Atendente_Lista.html', {'usuario_logado': usuario_logado})


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


@login_required
def reg_atend_busca_cliente(request):
    usuario_logado = request.user.username
    dado_pesquisa_nome = request.POST.get('sel_cliente')
   
    cons_depto = Departamento.objects.all()
    data_e_hora = datetime.now()

    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    page = request.GET.get('page')

    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        cliente_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa)
        paginas = Paginator(cliente_lista, 3)
        clientes = paginas.get_page(page)
        
        messages.info(request, 'Registro do atendimento de ' + dado_pesquisa  +' foi feito com sucesso')
        
        return render(request, 'Reg_Atendimento_busca.html', {'dados_cliente': clientes, 'dado_pesquisa':dado_pesquisa, 'dado_pesquisa_nome': dado_pesquisa_nome, 'cons_depto':cons_depto, 'data_e_hora':data_e_hora, 'usuario_logado': usuario_logado})


    if dado_pesquisa_nome != None and dado_pesquisa_nome != '':
        clientes_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        paginas = Paginator(clientes_lista, 3)
        page = request.GET.get('page')
        clientes = paginas.get_page(page)

        return render(request, 'Reg_Atendimento_busca.html', {'dados_cliente': clientes, 'sel_cliente': dado_pesquisa_nome, 'cons_depto': cons_depto, 'data_e_hora': data_e_hora, 'usuario_logado': usuario_logado})


    else:
        return render(request, 'Reg_Atendimento_busca.html', {'dados_cliente': dado_pesquisa_nome, 'usuario_logado': usuario_logado})
    
    
@login_required   
def sel_cliente(request, id):
    usuario_logado = request.user.username
    data_e_hora = datetime.now()

    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")
   
    cons_depto = Departamento.objects.all()
    dados_clientes = get_object_or_404(Cliente, pk=id)

    return render(request, 'Reg_Atendimento_busca.html', {'dados_cliente': dados_clientes, 'usuario_logado': usuario_logado, 'cons_depto':cons_depto, 'data_e_hora':data_e_hora})


@login_required
def salvar_atendimento_novo(request):
    usuario_logado = request.user.username
    id_atendente = request.user.id

    if request.method == 'POST':
        solicitacao = request.POST.get('solicitacao')
        clienteId = request.POST.get('id_cliente')
        departamento = request.POST.get('encaminhar')
        
        print('Meu print ', clienteId)

        cliente = Cliente.objects.get(id=clienteId)

        if departamento:
            departamento = Departamento.objects.get(id=departamento)
        else:
            departamento = None

        situacao = Situacao.objects.get(id=1)
        atendente = Atendente.objects.filter(user_atend_id=id_atendente).last()

        grava_atendimento = Atendimento(
            solicitacao=solicitacao,
            cliente=cliente,
            departamento=departamento,
            atendente=atendente,
            criado_em=datetime.now(),
            encerrado=0
        )

        grava_atendimento.save()
        cons_ultimo = Atendimento.objects.last()
        comentario = "Registro automático ao criar o chamado"
        atendimento = Atendimento.objects.get(id=cons_ultimo.id)

        grava_situacao_atendimento = Situacao_Atendimento(
            id_situacao=situacao,
            id_atendimento=atendimento,
            comentario=comentario,
            data_hora=datetime.now()
        )

        grava_situacao_atendimento.save()

        messages.info(request, f'Atendimento {str(cons_ultimo.id)} registrado com sucesso.')
        return redirect('reg_atend_busca_cliente')


@login_required
def reg_atend_api(request):
    usuario_logado = request.user.username
    cons_users = User.objects.all()
    cons_depto = Departamento.objects.all()

    data_e_hora = datetime.now()

    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    return render(request, 'Reg_Atendimento_busca.html', {'usuario_logado': usuario_logado,
                                                          'cons_users': cons_users,
                                                          'cons_depto': cons_depto,
                                                          'data_e_hora': data_e_hora})


@login_required
def cons_lista_atendimento(request):
    usuario_logado = request.user.username

    dado_pesquisa_numero = request.POST.get('numero')

    if dado_pesquisa_numero:
        atendimento = Atendimento.objects.filter(id=dado_pesquisa_numero)
        if atendimento:
            return render(request, 'Cons_Atendimento.html', {
                'atendimento': atendimento,
                'dado_pesquisa_numero': dado_pesquisa_numero
            })
    else:
        ultimo_atendimento = Atendimento.objects.last()
        seis_ultimos = ultimo_atendimento.id - 5

        atendimento = Atendimento.objects.filter(id__gte=seis_ultimos).order_by('-id')
        return render(request, 'Cons_Lista_Atendimento.html', {'Atendimento': atendimento,
                                                               'usuario_logado': usuario_logado})


@login_required
def cons_atendimento(request, id):
    usuario_logado = request.user.username
    atendimento = Atendimento.objects.get(id=id)
    cons_depto = Departamento.objects.all()
    cons_situ = Situacao.objects.all()

    cons_situ_atendimento = Situacao_Atendimento.objects.filter(id_atendimento=id).values("comentario", "data_e_hora",
                                                                        "id_situacao__descricao_situacao",
                                                                        "id_situacao__departamento__descricao_departamento",
                                                                        "id_atendimento__atendente__nome_atend").order_by('-id')

    return render(
        request,
        'Cons_Atendimento.html',
        {'atendimento': atendimento,
         'cons_situ_atendimento': cons_situ_atendimento,
         'cons_depto': cons_depto,
         'cons_situ': cons_situ,
         'usuario_logado': usuario_logado}
        )

