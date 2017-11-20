import os
import platform
if "Windows" == platform.system():
    import wmi
    import _winreg
import socket
import re

from paramiko.ssh_exception import SSHException, NoValidConnectionsError
from pprint import pprint
from sets import Set
from django.conf import settings
from paramiko.client import SSHClient, AutoAddPolicy



class WmiWorker():

    """docstring for WmiWorker"""
    def __init__(self, hostname, username, password,mac = None):
        # print("Connect to " + hostname)
        self.hostname = hostname
        self.username = username
        self.password = password
        if hostname.lower() in settings.LOCALHOSTS:
            self.worker = wmi.WMI()
        else:
            try:
                self.worker = wmi.WMI(hostname, user=self.username, password=self.password)
            except Exception as e:
                self.worker = None
                self.establish_error = str(e)
        # Validate MAC address
        """IP could be released by a computer and be leased by another one."""
        if mac != None and self.worker != None:
            valid_mac = False
            macs = self.getMacs()
            if macs == None:
                self.worker = None
                self.establish_error = 'Cannot execute command on client. Please check the permission'
            else:   
                for mac_addr in macs:
                    if mac.lower() == mac_addr.replace(":",'').lower():
                        valid_mac = True
                        break
                if not valid_mac:
                    self.worker = None
                    self.establish_error = 'MAC Address: ' + mac + ' is invalid'


    """Get MAC address of all network adapters"""
    def getMacs(self):
        macs=[]
        try:
            for interface in self.worker.Win32_NetworkAdapterConfiguration(IPEnabled=1):
                macs.append(interface.MACAddress)
        except Exception as e:
            return None
        return macs


    """Get all installed softwares and theirs version"""
    def getSoftwareList(self):
        reg_reader = self.worker.StdRegProv
        REG_KEYS_LIST = [
                'Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall', 
                'Software\Microsoft\Windows\CurrentVersion\Uninstall'
            ]

        softwares = Set()
        for reg_key in REG_KEYS_LIST:
            result, subkeys = reg_reader.EnumKey(hDefKey=_winreg.HKEY_LOCAL_MACHINE, sSubKeyName=reg_key)
            for subkey in subkeys:
                result, raw_display_name = reg_reader.GetStringValue(hDefKey=_winreg.HKEY_LOCAL_MACHINE, sSubKeyName=reg_key + "\\" + subkey, sValueName='DisplayName')
                if raw_display_name != None:
                    display_version = ''
                    result, display_version = reg_reader.GetStringValue(hDefKey=_winreg.HKEY_LOCAL_MACHINE, sSubKeyName=reg_key + "\\" + subkey, sValueName='DisplayVersion')
                    softwares.add((raw_display_name, display_version))
        return softwares


    """ Get current Operating System and its version"""
    def getOSVersion(self):
        if self.worker == None:
            return 'UNKNOWN'
        users = []
        for os in self.worker.Win32_OperatingSystem():
            if len(os.Name) > 0:
                return os.Name.split('|')[0]
            else:
                return ''


    """ Check whether Bitlocker Encryption is enabled or not. Return False if there is any volumne on it bitlocker is disabled"""
    def isBitLock(self):
        if self.hostname.lower() in settings.LOCALHOSTS:
            moniker = r"winmgmts:{impersonationLevel=impersonate,authenticationLevel=pktPrivacy}!root\cimv2\Security\MicrosoftVolumeEncryption"
            try:
                self.volume_encryption_worker = wmi.WMI(moniker=moniker)
            except Exception as e:
                return False
        else:
            moniker = r"winmgmts:{impersonationLevel=impersonate,authenticationLevel=pktPrivacy}!\\"+ self.hostname +r"\root\cimv2\Security\MicrosoftVolumeEncryption"
            self.volume_encryption_worker = wmi.WMI(moniker = moniker, user= self.username, password=self.password)
        protection_statuses = []
        for volume in self.volume_encryption_worker.Win32_EncryptableVolume():
            if volume.DriveLetter != None:
                protection_statuses.append(volume.ProtectionStatus)
        if sum(protection_statuses) == 0:
            return 0
        if sum(protection_statuses) == len(protection_statuses):
            return 1
        return 2

    def isDiskEncryption(self):
        is_bitlock = self.isBitLock()
        if is_bitlock == 0:
            softwares = self.getSoftwareList()
            for software in softwares:
                if 'Check Point Endpoint Security' in list(software)[0]:
                    return ['Checkpoint', 1]
            return ['Unencrypted', is_bitlock]
        else:
            return ['BitLocker', is_bitlock]
    # Check Point Endpoint Security

class SSHWorker(SSHClient):
    """docstring for SSHWorker"""
    def __init__(self, hostname = None, username = None, password = None, key_filename=None, mac=None, timeout =5):
        super(SSHWorker, self).__init__()
        self.is_established = False
        if hostname != None and username != None and password != None:
            self.set_missing_host_key_policy(AutoAddPolicy)
            self.hostname = hostname
            self.username = username
            self.password = password
            self.timeout = timeout
            try:
                self.connect(self.hostname, username = self.username, password = self.password, timeout = self.timeout)
                self.is_established = True
            except socket.timeout:
                self.is_established = False
                self.establish_error = "SSH channel timeout exceeded."
            except (SSHException, NoValidConnectionsError) as e:
                self.establish_error = str(e)
            
            if not self.is_established and key_filename != None:
                print("Fail to login with password! Retry with key")
                try:
                    # print("IP:" + hostname + " - Key file: "+ key_filename)
                    self.connect(self.hostname, username = self.username, key_filename = key_filename, timeout = self.timeout)
                    self.is_established = True
                except socket.timeout:
                    self.establish_error = "SSH channel timeout exceeded."
                except (SSHException, NoValidConnectionsError) as e:
                    self.establish_error = str(e)
            if self.is_established and mac != None:
                if not self._validateMAC(mac):
                    self.is_established = False
                    self.establish_error = 'MAC Address: ' + mac + ' is invalid'
                


    def isFileVault(self):
        command = 'fdesetup status 2>&1'
        try:
            stdin, stdout, stderr = self.exec_command(command)
        except SSHException as e:
            print("Cannot execute command. Detail: " + str(e))
            return None
        output = stdout.readlines()
        status = output[0].split(" ")[2].strip()
        if status != "On.":
            return 0
        if len(output) == 2:
            return 1
        else:
            return 2

    def getMacs(self):
        command = 'ifconfig 2>&1'
        try:
            stdin, stdout, stderr = self.exec_command(command)
        except SSHException as e:
            print("Cannot execute command. Detail: " + str(e))
            return None
        output = stdout.readlines()
        macs= []
        regex = re.compile(r'[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}')
        for line in output:
            line = line.strip()
            if regex.search(line):
                for word in line.split(" "):
                    if regex.search(word):
                        macs.append(word)
        return macs

    def _validateMAC(self, mac):
        valid_mac = False
        for mac_addr in self.getMacs():
            # print(mac_addr.replace(":",'').lower())
            if mac.lower() == mac_addr.replace(":",'').lower():
                valid_mac = True
                break
        return valid_mac
            
            

    
        
        