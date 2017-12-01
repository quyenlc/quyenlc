from django.core.management.base import BaseCommand, CommandError
from amsx.utils import Google

class Command(BaseCommand):

    def handle(self, *args, **options):
        # ...
        self.stdout.write(self.style.SUCCESS("Test is done. Goodbye "), ending='\n')
