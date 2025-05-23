from django.urls import path
from . import views

urlpatterns = [
    path('add_produto/', views.add_produto, name="add_produto"),
    path('listar_produtos/', views.listar_produtos, name="listar_produtos"),
    path('produto/<slug:slug>/', views.produto, name="produto"),
]
