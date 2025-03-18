from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Добавляет тестовых пользователей в группу 'manager'"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="manager")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'manager' создана."))

        users_data = [
            {"email": "manager1@email.com", "password": "password123"},
            {"email": "manager2@email.com", "password": "password123"},
            {"email": "manager3@email.com", "password": "password123"},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(email=user_data["email"])
            if created:
                user.set_password(user_data["password"])
                user.is_active = True
                user.save()
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f"Пользователь {user.email} "
                                                     f"создан и добавлен в группу 'manager'"))
            else:
                self.stdout.write(self.style.WARNING(f"Пользователь {user.email} уже существует."))

        self.stdout.write(self.style.SUCCESS("Добавление пользователей в группу 'manager' завершено."))
