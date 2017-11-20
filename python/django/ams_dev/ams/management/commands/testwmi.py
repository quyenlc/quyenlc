from django.core.management.base import BaseCommand, CommandError
from ams.utils import WmiWorker
from pprint import pprint
import wmi

class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.conf import settings
        
        radar_user = settings.RADAR_USER
        radar_pass = settings.RADAR_PASS
        test_hostname = 'VNHAN-00178-WIN'
        # test_hostname = 'localhost'
        # self.stdout.write(self.style.SUCCESS("User: " + radar_user + " - Password:" + radar_pass))
        worker = WmiWorker(test_hostname, radar_user, radar_pass)
        softwares = worker.getSoftwareList()
        pprint(softwares)
