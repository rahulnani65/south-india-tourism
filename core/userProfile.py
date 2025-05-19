from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile objects for users who do not have one'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            try:
                user.profile
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created UserProfile for {user.username}'))
            else:
                self.stdout.write(f'UserProfile already exists for {user.username}')