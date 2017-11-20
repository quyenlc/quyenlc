from django.core.management.base import BaseCommand, CommandError
from ams.utils import SSHWorker
from paramiko.ssh_exception import SSHException
from paramiko.client import AutoAddPolicy
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.conf import settings
        
        ip = '172.21.150.126'
        ssh_user = settings.SSH_USER
        ssh_pass = settings.SSH_PASS
        ssh_key = settings.SSH_KEY
        client = SSHWorker(ip, ssh_user, ssh_pass, ssh_key, 'b8e8564a4e8e')
        if client.is_established:
            macs=client.getMacs()
            print(macs)
        else:
            pprint(client.establish_error)
        client.close()

