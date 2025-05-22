from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users
from rolepermissions.roles import assign_role

@receiver(post_save, sender=Users)
def define_permissoes(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] Criou usuário {instance.username} com cargo {instance.cargo}")
        if instance.cargo == "V":
            assign_role(instance, 'vendedor')
            print("[Signal] Atribuiu papel Vendedor")
        elif instance.cargo == "G":
            assign_role(instance, 'gerente')
            print("[Signal] Atribuiu papel Gerente")
