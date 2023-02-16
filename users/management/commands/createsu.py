import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
User = get_user_model()


DJANGO_ADMIN_PASS = os.environ.get('DJANGO_ADMIN_PASS')

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if not User.objects.filter(username="ioniqadmin@turnonheat.com").exists():
            User.objects.create_superuser("ioniqadmin@turnonheat.com", DJANGO_ADMIN_PASS)