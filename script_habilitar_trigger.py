#!/usr/bin/env python3

# Script para comparar informações e ativar triggers após o termino de sua manutenção no Zabbix
# Versão v1.0

from zabbix_api import ZabbixAPI
from datetime import datetime

url = 'https://zabbix.com.br/zabbix/api_jsonrpc.php'
login = 'zabbix'
senha = 'zabbix'

zapi = ZabbixAPI(url, timeout=180)
zapi.validate_certs=False
zapi.login(login, senha)

datenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open("logmanut.log") as origin_file:
    for line in origin_file.readlines():
        if 'triggerid' in line:
            trigger = line.strip().split(': ')[1]
        if 'datafim' in line:
            datafinal = line.strip().split(': ')[1]
            if datafinal < datenow:
                zapi.trigger.update({
                    "triggerid": trigger,
                    "comments": "",
                    "status": 0
                })
