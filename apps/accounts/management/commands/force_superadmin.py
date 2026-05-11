from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Force-create or reset the SSEMATA superadmin account."

    def handle(self, *args, **options):
        username = "SSEMATA"
        email    = "ssematasabira24@gmail.com"
        password = "sabira@25"

        # Delete any existing user with same username (any case) or email to avoid conflicts
        User.objects.filter(username__iexact=username).delete()
        User.objects.filter(email=email).delete()

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name="SSEMATA",
            last_name="SABIRA",
        )
        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"SUCCESS: Superadmin '{username}' created fresh."
            f" Email: {email} | Password: {password}"
        ))
