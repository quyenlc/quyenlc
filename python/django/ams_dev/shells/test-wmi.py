import os
import wmi
import _winreg
from pprint import pprint
from sets import Set

user        = 'radar.ams'#os.getenv('DOMAIN_USER')
password    = '123456a@A'#os.getenv('password')
hostname = 'HAN-DCS-01'

def initWorker(hostname):
    if hostname.lower() == "han-dcs-02":
        wmi_worker = wmi.WMI()
    else:
        wmi_worker = wmi.WMI(hostname, user=user, password=password)
    return wmi_worker

def getMacs(hostname):
    macs = []
    wmi_worker = initWorker(hostname)
    for interface in wmi_worker.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        macs.append(interface.MACAddress)
    return macs

def getSoftwareList(hostname):
    wmi_worker = initWorker(hostname)
    reg_reader = wmi_worker.StdRegProv
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

def getOS(hostname):
    users = []
    wmi_worker = initWorker(hostname)
    for os in wmi_worker.Win32_OperatingSystem():
        if len(os.Name) > 0:
            return os.Name.split("|")[0]

softwares = getSoftwareList(hostname)
for software in softwares:
    pprint(list(software)[0])
    

