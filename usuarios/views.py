from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rolepermissions.decorators import has_permission_decorator
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rolepermissions.checkers import has_permission

from .models import Users
from .forms import VendedorForm
from estoque.models import Produto
from estoque.forms import ProdutoForm


@login_required
def plataforma_view(request):
    """Renderiza a página principal da plataforma ou redireciona vendedores."""
    user = request.user

    if user.cargo == 'V':  # Se for vendedor, redireciona direto para cadastro de produtos
        return redirect('add_produto')

    return render(request, 'plataforma.html')


@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor_view(request):
    """Permite cadastrar um novo vendedor com paginação e ordenação."""
    form = VendedorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vendedor cadastrado com sucesso.")
        return redirect('cadastrar_vendedor')
    elif request.method == "POST":
        messages.error(request, "Corrija os erros abaixo.")

    sort = request.GET.get('sort', 'first_name')
    vendedores_list = Users.objects.filter(cargo="V").order_by(sort)
    paginator = Paginator(vendedores_list, 10)
    page_number = request.GET.get('page')
    vendedores = paginator.get_page(page_number)

    return render(request, 'cadastrar_vendedor.html', {
        'vendedores': vendedores,
        'form': form
    })


@has_permission_decorator('cadastrar_produtos')
def add_produto_view(request):
    """Permite cadastrar um novo produto."""
    form = ProdutoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto cadastrado com sucesso.")
        return redirect('add_produto')
    elif request.method == "POST":
        messages.error(request, "Corrija os erros abaixo.")

    produtos = Produto.objects.all()

    return render(request, 'add_produto.html', {
        'form': form,
        'produtos': produtos,
    })


def login_view(request):
    """Autentica o usuário e o redireciona para a plataforma."""
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('plataforma')
        return render(request, 'login.html')

    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('login')

        auth.login(request, user)
        messages.success(request, "Login realizado com sucesso.")
        return redirect('plataforma')


def logout_view(request):
    """Efetua logout do usuário."""
    auth.logout(request)
    messages.info(request, "Você saiu da plataforma.")
    return redirect('login')


@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario_view(request, id):
    """Exclui um vendedor com base no ID."""
    vendedor = get_object_or_404(Users, id=id)
    vendedor.delete()
    messages.success(request, "Vendedor excluído com sucesso.")
    return redirect('cadastrar_vendedor')
