from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('plataforma/', views.plataforma_view, name="plataforma"),
    path('cadastrar_vendedor/', views.cadastrar_vendedor_view, name="cadastrar_vendedor"),
    path('excluir_usuario/<int:id>/', views.excluir_usuario_view, name="excluir_usuario"),
    path('add_produto/', views.add_produto_view, name="add_produto"),
]
