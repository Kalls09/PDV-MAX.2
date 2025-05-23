from django.urls import path
from . import views

urlpatterns = [
    path('realizar/', views.realizar_venda, name='realizar_venda'),
    path('logs/', views.listar_logs, name='listar_logs'),
    path('detalhe/<int:venda_id>/', views.detalhe_venda, name='detalhe_venda'),
]
