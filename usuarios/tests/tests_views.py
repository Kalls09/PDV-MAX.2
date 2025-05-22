import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from usuarios.models import Users

@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_user(
        username="admin@example.com",
        email="admin@example.com",
        password="adminpass",
        cargo="A"  # Ajuste se 'A' não for admin
    )

@pytest.fixture
def client_logged(admin_user):
    client = Client()
    client.login(username=admin_user.username, password="adminpass")
    return client

@pytest.mark.django_db
def test_login_view_ok(client):
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cadastrar_vendedor_get(client_logged):
    url = reverse("cadastrar_vendedor")
    response = client_logged.get(url)
    assert response.status_code == 200
    assert "Vendedores Cadastrados" in response.content.decode()

@pytest.mark.django_db
def test_cadastrar_vendedor_post(client_logged):
    url = reverse("cadastrar_vendedor")
    response = client_logged.post(url, {
        "first_name": "João",
        "last_name": "Silva",
        "email": "joao@email.com",
        "senha": "Senha123@"
    })
    assert response.status_code == 302  # redirect
    assert Users.objects.filter(email="joao@email.com").exists()

@pytest.mark.django_db
def test_excluir_usuario_view(client_logged):
    vendedor = Users.objects.create_user(
        username="vend1@email.com",
        email="vend1@email.com",
        password="testepass123",
        first_name="Vend",
        last_name="Um",
        cargo="V"
    )
    url = reverse("excluir_usuario", args=[vendedor.id])
    response = client_logged.post(url)
    assert response.status_code == 302
    assert not Users.objects.filter(id=vendedor.id).exists()
