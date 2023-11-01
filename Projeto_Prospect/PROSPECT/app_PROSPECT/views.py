from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Cliente, Atendente
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage


def abre_index(request):
    return render(request, 'index.html')


@login_required
def cad_cliente(request):
    return render(request, 'cad_cliente.html')


@login_required
def salvar_cliente_novo_prospect(request):
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
        messages.info(request, 'O cliente ' + nome+' foi cadastrao com sucesso!' )
        return render(request, 'cad_cliente.html')


@login_required
def cons_cliente_prospect(request):
    dado_pesquisa_nome = request.POST.get('cliente')
    dado_pesquisa_telefone = request.POST.get('telefone')
    dado_pesquisa_email = request.POST.get('email')

    page = request.GET.get('page')

    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        clientes_lista = Cliente.objects.filter(nome__icontain=dado_pesquisa)
        paginas = Paginator(clientes_lista, 3)
        clientes = paginas.get_page(page)
        return render(request, 'Cons_Cliente_Lista', {'dados_cliente': clientes, 'dado_pesquisa': dado_pesquisa_nome})




    if dado_pesquisa_nome != None and dado_pesquisa_nome != '':
        clientes_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)

        paginas = Paginator(clientes_lista, 3)
        page = request.GET.get('page')
        clientes = paginas.get_page(page)

        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': clientes, 'dado_pesquisa': dado_pesquisa_nome})

    elif dado_pesquisa_telefone != None and dado_pesquisa_telefone != '':
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_telefone)
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': clientes})

    elif dado_pesquisa_email != None and dado_pesquisa_email != '':
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_email)
        return render(request, 'Cons_Cliente_Lista.html', {'dados_clientes': clientes})

    else:
        return render(request, 'Cons_Cliente_Lista.html')


def edit_cliente(request, id):
    dados_entrar = get_object_or_404(Cliente, pk=id)
    return render(request, 'Edit_Cliente.html', {'dados_clientes': dados_entrar})


def salvar_cliente_editado(request):
    if request.method == 'POST':
        id_cliente = request.POST.get('id_cliente')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        observacao = request.POST.get('observacao')

        Cliente_editado = Cliente.objects.get(id=id_cliente)

        Cliente_editado.nome = nome
        Cliente_editado.email = email
        Cliente_editado.telefone = telefone
        Cliente_editado.observacao = observacao

        Cliente_editado.save()
        messages.info(request,'Cliente '+nome+' editado com sucesso')
        return render(request, 'Edit_cliente.html')


@login_required
def delete_cliente(request, id):
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()

    messages.info(request, 'Cliente ' + nome + ' excluido com sucesso!')
    return redirect('cons_cliente_prospect')


# def lista_paginas(request):
#     itens = Cliente.objects.all().order_by('-created_at')
#     paginator = Paginator(itens, 5)
#
#     numero_pagina = request.GET.get('pagina')
#     page = paginator.get_pagina(numero_pagina)
#
#     return render(request, 'pagina.html', {'page': page})

@login_required
def salvar_atend_novo(request):
    usuario_logado = request.user.username

    if request.method =='POST':
        nome_atend = request.POST.get('nome_atend')
        telefone_atend = request.POST.get('telefone_atend')
        user_atend = request.POST.get('user_atend')
        observacao_atend = request.POST.get('observacao_atend')

        if user_atend:
            user_atend=User.objects.get(username=user_atend)
        else:
            user_atend = None

        grava_atend = Atendente(
            nome_atend = nome_atend,
            telefone_atend = telefone_atend,
            observacao_atend = observacao_atend,
            ativo_atend = 1,
            user_atend = user_atend
        )

        grava_atend.save()
        messages.info(request, 'Atendente '+ nome_atend +' cadastrado com sucesso!', 'cad_atend', {'usuario_logado': usuario_logado})


@login_required
def cad_atend(request):
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})

