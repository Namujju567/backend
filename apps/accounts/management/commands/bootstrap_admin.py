from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

TEMP_USERNAME = "admin"
TEMP_EMAIL    = "admin@gmail.com"
TEMP_PASSWORD = "admin123"


class Command(BaseCommand):
    help = "Bootstrap a temporary superadmin on first deploy. No-ops once a real superadmin exists."

    def handle(self, *args, **options):
        # If any superadmin OTHER than the temp account already exists,
        # the setup is complete — do nothing so real users are never touched again.
        real_superadmin_exists = User.objects.filter(
            is_superuser=True, is_active=True
        ).exclude(username=TEMP_USERNAME).exists()

        if real_superadmin_exists:
            self.stdout.write("bootstrap_admin: real superadmin found — skipping.")
            return

        # Create the temp superadmin if not present, always reset password
        if not User.objects.filter(username=TEMP_USERNAME).exists():
            User.objects.create_superuser(
                username=TEMP_USERNAME,
                email=TEMP_EMAIL,
                password=TEMP_PASSWORD,
            )
            self.stdout.write(self.style.SUCCESS(
                f"Superadmin '{TEMP_USERNAME}' created."
            ))
        else:
            u = User.objects.get(username=TEMP_USERNAME)
            u.is_active = True
            u.is_staff = True
            u.is_superuser = True
            u.set_password(TEMP_PASSWORD)  # always reset so login works
            u.save()
            self.stdout.write(self.style.WARNING(
                f"Superadmin '{TEMP_USERNAME}' already exists — password reset, ensured active."
            ))

        # Disable every other user so only the temp account can log in
        disabled = User.objects.exclude(username=TEMP_USERNAME).update(is_active=False)
        self.stdout.write(self.style.SUCCESS(
            f"{disabled} other user(s) disabled."
        ))

        self.stdout.write(self.style.SUCCESS(
            "\nLog in as:\n"
            f"  username : {TEMP_USERNAME}\n"
            f"  password : {TEMP_PASSWORD}\n"
            "Go to Settings > Access Control, create your real superadmin,\n"
            "then delete this temp account."
        ))
