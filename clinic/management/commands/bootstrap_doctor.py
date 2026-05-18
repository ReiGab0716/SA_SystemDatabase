import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from clinic.models import Profile


class Command(BaseCommand):
    help = "Create or update a doctor account from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DOCTOR_USERNAME", "").strip()
        password = os.environ.get("DOCTOR_PASSWORD", "")
        email = os.environ.get("DOCTOR_EMAIL", "").strip()
        first_name = os.environ.get("DOCTOR_FIRST_NAME", "Doctor").strip()
        last_name = os.environ.get("DOCTOR_LAST_NAME", "Account").strip()

        if not username or not password:
            raise CommandError("Set DOCTOR_USERNAME and DOCTOR_PASSWORD to bootstrap a doctor account.")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": True,
            },
        )

        changed = created

        if email and user.email != email:
            user.email = email
            changed = True
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            changed = True
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            changed = True
        if not user.is_staff:
            user.is_staff = True
            changed = True

        user.set_password(password)
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        if profile.role != "DOCTOR":
            profile.role = "DOCTOR"
            profile.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} doctor account: {username}"))
