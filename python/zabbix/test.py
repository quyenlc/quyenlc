from zabbix_api import ZabbixAPI
from pprint import pprint
zapi = ZabbixAPI(server="http://mon.marvel.denagames-asia.com/zabbix")
username = 'infra'
password = 'Punch123!'

zapi.login(username, password)

hosts = zapi.host.get({'groupids': '14', 'search': {'host':'ult-n-rds'}, 'output':'extend'})
# for host in (hosts):
    # pprint(host)
items = zapi.item.get({'hostids':hosts[0]['hostid'], "output": "extend"})
for item in items:
    print item['name']
    