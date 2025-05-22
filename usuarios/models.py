from django.db import models
from django.contrib.auth.models import AbstractUser
from rolepermissions.roles import assign_role

#user = Users.objects.get(email='email_do_gerente@email.com')
#assign_role(user, 'gerente')


class Users(AbstractUser):
    choices_cargo = (('V', 'Vendedor'),
                     ('G', 'Gerente'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)