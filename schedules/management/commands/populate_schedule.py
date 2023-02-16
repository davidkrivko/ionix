import os
from django.core.management.base import BaseCommand, CommandError
from schedules.utils import populate_schedule_options

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        populate_schedule_options()