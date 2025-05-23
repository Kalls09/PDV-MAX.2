from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.db import transaction
from .models import Venda, ItemVenda, VendaLog
from .forms import ItemVendaForm
from django.contrib.auth.decorators import login_required


def realizar_venda(request):
    ItemVendaFormSet = formset_factory(ItemVendaForm, extra=1)

    if request.method == 'POST':
        formset = ItemVendaFormSet(request.POST)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    venda = Venda.objects.create(vendedor=request.user)
                    total = 0

                    for form in formset:
                        produto = form.cleaned_data.get('produto')
                        quantidade = form.cleaned_data.get('quantidade')

                        if produto and quantidade:
                            if produto.quantidade < quantidade:
                                messages.error(request, f'Estoque insuficiente para {produto.nome}.')
                                raise Exception('Estoque insuficiente')

                            preco = produto.preco_venda
                            subtotal = preco * quantidade
                            total += subtotal

                            # Atualizar estoque
                            produto.quantidade -= quantidade
                            produto.save()

                            ItemVenda.objects.create(
                                venda=venda,
                                produto=produto,
                                quantidade=quantidade,
                                preco_unitario=preco,
                                subtotal=subtotal
                            )

                    venda.valor_total = total
                    venda.save()

                    VendaLog.objects.create(
                        venda=venda,
                        usuario=request.user,
                        valor_total=total,
                        observacao='Venda realizada com sucesso via formulário.'
                    )

                    messages.success(request, 'Venda realizada com sucesso!')
                    return redirect('listar_produtos')

            except Exception as e:
                messages.error(request, 'Erro ao realizar venda.')

    else:
        formset = ItemVendaFormSet()

    return render(request, 'vendas/realizar_venda.html', {
        'formset': formset
    })


@login_required
def listar_logs(request):
    logs = VendaLog.objects.select_related('venda', 'usuario').order_by('-data_hora')

    # Para cada log, vamos buscar os itens relacionados da venda e passar junto
    logs_com_detalhes = []
    for log in logs:
        itens = log.venda.itens.all()  # todos os itens daquela venda
        logs_com_detalhes.append({
            'log': log,
            'itens': itens
        })

    return render(request, 'vendas/listar_logs.html', {'logs_com_detalhes': logs_com_detalhes})
