# zabbix-api-trigger-with-python

Sistema para criar manutenção de trigger no zabbix

O objetivo desse sistema é suprir uma necessidade que o zabbix não possui atualmente em suas versões, a de criar um período de manutenção para triggers específicas ao invés de colocar um host inteiro em manutenção.

Cito como destaque nesse script o consumo da api do zabbix com python utilizando os métodos 'trigger.get' e 'trigger.update'.
A utilização de estrutura de repetição, condições, exceções com 'try' e 'except', data/hora e gerenciamento de arquivos.

Contem dois scripts:

#### 1º script_manutencao_trigger.py
- Script que desativará a trigger informada e guardará as informações necessárias em 'logmanut.log' para ser reativada posteriormente e automaticamente pelo segundo script.

#### 2º script_habilitar_trigger.py
- Script que consultará o arquivo 'logmanut.log' procurando por períodos de manutenção concluídos para reativação da trigger automaticamente.
