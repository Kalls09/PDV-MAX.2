from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_vendedor': True,
        'cadastrar_produtos': True,
        'visualizar_produtos': True,
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
        'visualizar_produtos': True,
    }
