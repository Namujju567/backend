from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Force-create or reset the SSEMATA superadmin account."

    def handle(self, *args, **options):
        username = "SSEMATA"
        email    = "ssematasabira24@gmail.com"
        password = "sabira@25"

        user, created = User.objects.get_or_create(username=username)
        user.email      = email
        user.first_name = "SSEMATA"
        user.last_name  = "SABIRA"
        user.is_active  = True
        user.is_staff   = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "created" if created else "reset"
        self.stdout.write(self.style.SUCCESS(
            f"Superadmin '{username}' {action}. Login with password: {password}"
        ))
