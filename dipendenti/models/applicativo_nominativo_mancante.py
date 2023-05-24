import COCOZZA_connectDb
from COCOZZA_logs import PRINT, SALVA_LOG
import json


COCOZZA_connectDb.start()
with open('dipendenti_senza_contatto.txt', 'r') as f:
    content = f.read()
    # print(content)
    data = json.loads(content)


data = [
    {'name': 'FIORENTINO ANTONIO'},
    {'name': 'FRACASSO DAVIDE'},
    {'name': 'ASHAB SUPIEN'},
    {'name': 'ALIVERNINI ALESSANDRO'},
    {'name': 'PASQUALI MARCO'},
    {'name': 'PATRASC ROBERT COSMIN'},
    {'name': 'CARDONE GERARDO'},
    ]

for dipendente in data:
    PRINT("\nSTAMPO RECORD\n\n")
    PRINT(dipendente)
    name = dipendente['name']


    
    PRINT(name)    
    
    
    res_partner_id = COCOZZA_connectDb.sqlCreate('res.partner',
                                            { 
                                            'name': name,
                                            'is_company': False,
                                            'active': True
                                            })
    PRINT(f"Res.partner creato con successo. Il suo id è {res_partner_id[0]}")
    