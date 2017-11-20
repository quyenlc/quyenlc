from django.core.management.base import BaseCommand, CommandError
from ams.utils import WmiWorker, SSHWorker
from ams.models import ADComputer
from pprint import pprint
import wmi

class Command(BaseCommand):

    def scan(self,ad_computer):
        from django.conf import settings
        
        radar_user = settings.RADAR_USER
        radar_pass = settings.RADAR_PASS
        if ad_computer.getIP() == None:
            ad_computer.save()
            print "Stop scan computer " + ad_computer.name + " because its ip was not found"
            return None
        print("Scan computer " + ad_computer.name + "...")
        ad_computer.scan_status = 1
        ad_computer.save()
        for record in ad_computer.getIP():
            if ad_computer.scan_status == 2:
                return None
            ip = record['ip_addr']
            if '192.168.' in ip:
                ad_computer.scan_status = 0
                ad_computer.save()
                continue
            if ad_computer.getOSPlatform() == 'Mac':
                print("SSH to " + ip)
                ad_computer.os = 'Mac'
                ad_computer.fde_software = 'FileVault'
                ad_computer.scan_status = 1
                ad_computer.save()
                ssh_user = settings.SSH_USER
                ssh_pass = settings.SSH_PASS
                ssh_key = settings.SSH_KEY
                worker = SSHWorker(ip, ssh_user, ssh_pass, ssh_key)
                if worker.is_established:
                    ad_computer.scan_status = 2
                    ad_computer.note = ip
                    ad_computer.fde_status = worker.isFileVault()
                    ad_computer.save()
                else:
                    print("Could not establish connection. Error: " + worker.establish_error)
                    ad_computer.note = worker.establish_error
                    ad_computer.scan_status = 0
                    ad_computer.save()
                    continue
            elif ad_computer.getOSPlatform() == 'Win':
                # print("Hostname: " + ad_computer.name + " - IP:" + ip)
                # return None #Test
                print("Query WMI via IP: " + ip)
                worker = WmiWorker(ip, radar_user, radar_pass, record['mac_addr'])
                if worker.worker == None:
                    ad_computer.note = worker.establish_error
                    ad_computer.scan_status = 0
                    ad_computer.save()
                    continue
                ad_computer.os = worker.getOSVersion()
                ad_computer.scan_status = 2
                ad_computer.note = ip
                disk_status = worker.isDiskEncryption()
                ad_computer.fde_software = disk_status[0]
                ad_computer.fde_status = disk_status[1]
                ad_computer.save()
        return None
        print "--------- End ---------"


    def handle(self, *args, **options):
        # for ad_computer in ADComputer.objects.filter(scan_status__lte=1).exclude(fde_status__exact=1):
        # for ad_computer in ADComputer.objects.filter(name__icontains='vnhan-00170-win'):
        for ad_computer in ADComputer.objects.filter(scan_status__lte=1):
            self.scan(ad_computer)
