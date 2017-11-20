from django.core.management.base import BaseCommand, CommandError
from ams.models import ADComputer
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        for ad_computer in ADComputer.objects.filter(scan_status__lte=2):
            ad_computer.scan_status = 0
            ad_computer.save()
        