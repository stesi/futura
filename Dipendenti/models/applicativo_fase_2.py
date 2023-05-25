import COCOZZA_connectDb
from COCOZZA_logs import PRINT, SALVA_LOG
import json


COCOZZA_connectDb.start()
with open('dipendenti_senza_contatto.txt', 'r') as f:
    content = f.read()
    # print(content)
    data = json.loads(content)


for dipendente in data:
    PRINT("\nSTAMPO RECORD\n\n")
    PRINT(dipendente)
    employee_id = dipendente['id']
    name = dipendente['name']
    pwork_cf = dipendente['pwork_cf']
    first_name = dipendente['first_name']
    last_name = dipendente['last_name']

    
    PRINT(employee_id)    
    PRINT(name)    
    PRINT(pwork_cf)    
    
    
    # # Controllo se esiste un res.partner con lo stesso nome e i primi 14 caratteri del codice fiscale
    # res_partner_cf = COCOZZA_connectDb.sqlSearchMultiple('res.partner', [('name', 'ilike', name),('l10n_it_codice_fiscale', 'ilike', pwork_cf[0:14])])
    # PRINT(res_partner_cf[0]['id'])
    # # Se non esiste proseguo con la creazione del res.partner
    # if res_partner_cf != []:
    #     PRINT("Il res.partner non esiste. Procedo con la creazione.")
    #     res_partner_id = COCOZZA_connectDb.sqlCreate('res.partner',
    #                                                 { 
    #                                                 'name': name,
    #                                                 'first_name': first_name,
    #                                                 'last_name': last_name,
    #                                                 'is_company': False,
    #                                                 })
    #     PRINT(f"Res.partner creato con successo. Il suo id è {res_partner_id[0]}")
    #     COCOZZA_connectDb.sqlWrite('hr.employee', [[employee_id], {'address_home_id': res_partner_id[0]}])
    #     PRINT(f"Res.partner con id {res_partner_id} associato con hr.employee {employee_id} correttamente.")
    
    # res_partner_ = COCOZZA_connectDb.sqlSearchMultiple('res.partner', [('name', 'ilike', name),('l10n_it_codice_fiscale', 'ilike', pwork_cf[0:14])])
    # PRINT(res_partner[0]['id'])
    # if res_partner 
    #     # Se esiste associo hr.employee al res.partner
    #     PRINT(f"Il res.partner è già esistente. Procedo con l'associazione")
    #     COCOZZA_connectDb.sqlWrite('hr.employee', [[employee_id], {'address_home_id': res_partner[0]['id']}])
    #     PRINT(f"Res.partner con id {res_partner_cf[0]['id']} associato con hr.employee {employee_id} correttamente.")

    
    
    
    
    
    # Controllo se nome e codice fiscale sono esistenti
    res_partner_cf = COCOZZA_connectDb.sqlSearchMultiple('res.partner', [('name', 'ilike', name),('l10n_it_codice_fiscale', 'ilike', pwork_cf[0:14])])
    if res_partner_cf:
        PRINT(res_partner_cf[0]['id'])
    PRINT("controllo se esiste il res.partner con nome e codice fiscale inserito")
    if res_partner_cf == []:
        # NO -> Controllo se esiste un record con il nome e cognome
        PRINT("Il res.partner non esiste. Provo a cercarne uno con solo il nome corrispondente")
        res_partner = COCOZZA_connectDb.sqlSearch('res.partner', ['name', 'ilike', name],['id'])
        if res_partner == []:
            # NO -> Procedo alla creazione del res.partner e associo hr.employee
            PRINT("Anche in questo caso non esiste. Procedo alla creazione del res.partner e all'associazione con hr.employee")
            res_partner_id = COCOZZA_connectDb.sqlCreate('res.partner',
                                                    { 
                                                    'name': name,
                                                    'first_name': first_name,
                                                    'last_name': last_name,
                                                    'is_company': False,
                                                    })
            PRINT(f"Res.partner creato con successo. Il suo id è {res_partner_id[0]}")
            print(f"Stampo res_partner[0]['id'] =  {res_partner_id[0]}")
            COCOZZA_connectDb.sqlWrite('hr.employee', [[employee_id], {'address_home_id': res_partner_id[0]}])
            PRINT("Associazione eseguita correttamente.")
        else:
            # SI -> Procedo all'associazione del hr.employee al res.partner
            PRINT("Esiste. Procedo all'associazione tra res.partner e hr.employee")
            print(f"Stampo res_partner[0]['id'] =  {res_partner[0]['id']}")
            COCOZZA_connectDb.sqlWrite('hr.employee', [[employee_id], {'address_home_id': res_partner[0]['id']}])
            PRINT("Associazione eseguita correttamente.")
    else:
        # SI -> Associo hr.employee a res.partner
        PRINT("Il res.partner è esistente. Procedo all'associazione con hr.employee")
        print(f"Stampo res_partner_cf[0]['id'] =  {res_partner_cf[0]['id']}")
        COCOZZA_connectDb.sqlWrite('hr.employee', [[employee_id], {'address_home_id': res_partner_cf[0]['id']}])
        PRINT("Associazione eseguita correttamente.")