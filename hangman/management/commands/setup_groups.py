from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Setup groups"

    def handle(self, *args, **options):
        groups_names = ["professores", "alunos"]
        for group_name in groups_names:
            Group.objects.get_or_create(name=group_name)

        perms = ["add_tema", "change_tema", "delete_tema", "add_palavra"]
        professores = Group.objects.get(name="professores")
        professores.permissions.set(
            Permission.objects.get(codename=perm) for perm in perms
        )
