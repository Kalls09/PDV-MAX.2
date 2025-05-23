from django.db import models
from usuarios.models import Users
from estoque.models import Produto
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings



class Venda(models.Model):
    vendedor = models.ForeignKey(Users, on_delete=models.PROTECT)
    data = models.DateTimeField(default=datetime.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Venda {self.id} - {self.vendedor}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
    
class VendaLog(models.Model):
    venda = models.ForeignKey('Venda', on_delete=models.CASCADE, related_name='logs')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Log da venda #{self.venda.id} em {self.data_hora.strftime("%Y-%m-%d %H:%M:%S")}'
