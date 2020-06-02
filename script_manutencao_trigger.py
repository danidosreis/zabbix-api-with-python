#!/usr/bin/env python3

#########################################################################################
#                              Manutenção Trigger                                       #
#                                                                                       #
# Script para coletar informações e criar períodos de manutenção de triggers            #
# Versão v1.0                                                                           #
#                                                                                       #
#########################################################################################

from zabbix_api import ZabbixAPI
from datetime import datetime
import getpass

# Data e hora atual
datenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print()
print('\033[32m'+'#########################################################'+'\033[0;0m')
print('\033[32m'+'#              ZABBIX MANUTENÇÃO DE TRIGGERS            #'+'\033[0;0m')
print('\033[32m'+'#########################################################'+'\033[0;0m')

# Conexão API Zabbix
url = 'https://zabbix.com.br/api_jsonrpc.php'
zapi = ZabbixAPI(url)
zapi.validate_certs = False
print()

# Validação login Zabbix
while True:
    try:
        login = input('\033[36m'+'Login: '+'\033[0;0m')
        senha = getpass.getpass('\033[36m'+"Senha: "+'\033[0;0m')
        zapi.login(login, senha)
        break
    except:
        print('\033[31m'+"Usuário e senha inválidos, digite novamente."+'\033[0;0m')
        continue

# Validação triggerid
while True:
    triggerid = input('\033[36m'+'TrigerID: '+'\033[0;0m')
    if not triggerid.isdigit() or len(triggerid) > 8:
        print('\033[31m'+'Digite um triggerID válido.')
        continue
    else:
        triggerid = int(triggerid)
        # Get API para validar se triggerid existe no Zabbix
        get = zapi.trigger.get({
            "triggerids": triggerid,
            "output": ["description"],
            "selectHosts": ["name"]
        })
        if get == []:
            print('\033[31m'+'O triggerID digitado não existe no Zabbix, digite novamente.'+'\033[0;0m')
            continue
        else:
            break

# Validação chamado
while True:
    chamadoid = input('\033[36m'+'Chamado: '+'\033[0;0m')
    if not chamadoid.isdigit() or len(chamadoid) > 10:
        print('\033[31m'+'Digite um número de chamado válido.'+'\033[0;0m')
        continue
    else:
        chamadoid = int(chamadoid)
        break

# Validação data
while True:
    try:
        dataInicio = input('\033[36m'+'Data início da manutenção: [ dd/mm/aaa ] '+'\033[0;0m')
        dataFim = input('\033[36m'+'Data fim da manutenção: [ dd/mm/aaa ] '+'\033[0;0m')
        dataInicio = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataFim = datetime.strptime(dataFim, '%d/%m/%Y')
        break
    except:
        print('\033[31m'+'Por favor, digite uma data válida.'+'\033[0;0m')
        continue
print()

# Desativando trigger
update = zapi.trigger.update({
    "triggerid": triggerid,
    "comments": chamadoid,
    "status": 1
})

# Filtrando triggername e visiblename
triggername = get[0]['description']
host = get[0]['hosts'][0]['name']

print()
print('\033[32m' + '\033[1m' + 'O alerta "{}" do host "{}" foi suspenso da monitoração até a data "{}"'.format(triggername, host, dataFim)+'\033[0;0m')
print()

# Arquivo de log
arquivo = open('logmanut.log', 'a')
arquivo.write("\ntriggerid: {}".format(triggerid))
arquivo.write('\n')
arquivo.write("chamadoid: {}".format(chamadoid))
arquivo.write('\n')
arquivo.write("datainicio: {}".format(dataInicio))
arquivo.write('\n')
arquivo.write("datafim: {}".format(dataFim))
arquivo.write('\n')
arquivo.write("user: {}".format(login))
arquivo.write('\n')
arquivo.write("dateupdate: {}".format(datenow))
arquivo.write('\n')
arquivo.close()


# Deslogando Zabbix
zapi.logout()

