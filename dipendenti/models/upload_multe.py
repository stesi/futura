import openpyxl
import COCOZZA_connectDb
from COCOZZA_logs import PRINT, SALVA_LOG



# Apri il file Excel
workbook = openpyxl.load_workbook('./multe.xlsx')

# Seleziona il foglio di lavoro "pagina 1"
worksheet = workbook['MULTE']

# Leggi i titoli della tabella dalla riga 1, colonne A a W
titles = []
for column in range(1, 23):
    cell_value = worksheet.cell(row=1, column=column).value
    titles.append(cell_value)

# Leggi i dati delle righe successive, dalle celle A2 a Wn (n = numero di righe)
data = []
for row in range(2, worksheet.max_row + 1):
    row_data = {}
    for column in range(1, 23):
        cell_value = worksheet.cell(row=row, column=column).value
        row_data[titles[column - 1]] = cell_value
    data.append(row_data)

# Chiudi il file Excel
workbook.close()

# Fai qualcosa con i dati letti...
print(titles)


# COCOZZA_connectDb.start()



for record in data:
    PRINT("\nSTAMPO RECORD\n\n")
    PRINT(record)
    id_multa = record['IDMULTA']
    n_verbale = record['N° VERBALE']
    intestatario = record['INTESTATARIO']
    data_verbale = record['DATA VERBALE']
    ora_verbale = record['ORA']
    luogo = record['LUOGO']
    comune = record['CITTA\'']
    targa = record['TARGA']
    infrazione = record['INFRAZIONE']
    importo = record['IMPORTO']
    competenza = record['COMPETENZA']
    decurtazione_punti = record['DECURTAZIONE PUNTI']
    soggetto = record['SOGGETTO']
    note = record['INFRAZIONE']

    
    print(id_multa)    
    print(n_verbale)    
    print(intestatario)    
    print(data_verbale)    
    print(ora_verbale)    
    print(luogo)    
    print(comune)    
    print(targa)    
    print(infrazione)    
    print(importo)    
    print(competenza)    
    print(decurtazione_punti)    
    print(soggetto) 
    
    print(COCOZZA_connectDb.sqlSearch('res.partner',['name', 'ilike', soggetto]))
    


    # Recupero ID
    service_type_log_id = COCOZZA_connectDb.sqlSearch('fleet.service.type', ['name', '=', 'Multa'])
    vehicle_id = COCOZZA_connectDb.sqlSearch('fleet.vehicle', ['license_plate', '=', targa])
    res_partner_id = COCOZZA_connectDb.sqlSearch('res.partner', ['name', '=', soggetto])
    
    
    # Controlli anti interruzione con salvataggio dei record saltati
    if res_partner_id == []:
        SALVA_LOG("multe_saltate_dipendenti.txt", f"Il dipendente {soggetto} non esiste nei res.partner\n")
        continue
    if vehicle_id == []:
        SALVA_LOG("multe_saltate_veicoli.txt", f"Il veicolo con targa {targa} non esiste nel fleet.vehicle\n")
        continue
    
    
    
    # Sistemazione variabili
    if decurtazione_punti == None:
        punti = 0
        print("punto è settato a ZERO")
    else:
        punti = decurtazione_punti
        print("Punti è settato con il valore dell'Excel")

    
    #Saltare per problemi utenti
    
    saltare_soggetto = ['SENATORE ANTONIO', 'ZORDAN MASSIMO', "", "LOMBARDI SIMONE", "CAVE MICHELE", "DELLAL KARIM", "VECCHIETTI RUGGERO", "BELLASSAI EMILIANO"]
    saltare_targa = ['FB870DY', "EV096MK", "EY096MK"]
    
    if soggetto not in saltare_soggetto:
        if targa not in saltare_targa:
            if soggetto == "":
                print("")
            PRINT("Procedo con la creazione della seguente multa:\n")
            PRINT("N° verbale " + str(n_verbale) + " - id vecchio gestionale " + str(id_multa))
            PRINT(f"date = {service_type_log_id[0]['id']}")
            PRINT(f"amount = {importo}")
            PRINT(f"vehicle_id = {vehicle_id[0]['id']}")
            PRINT(f"Il soggetto è {soggetto}")
            PRINT(f"purchaser_id = {res_partner_id[0]['id']}")
            PRINT(f"deduction_point = {punti}")
            PRINT(f"notes = {note}")
            
            
            
        # Creazine record
            COCOZZA_connectDb.sqlCreate('fleet.vehicle.log.services', {
                'description': "N° verbale " + str(n_verbale) + " - id vecchio gestionale " + str(id_multa),
                'service_type_id': service_type_log_id[0]['id'],
                'date': str(data_verbale),
                'amount': importo,
                'vehicle_id': vehicle_id[0]['id'],
                'purchaser_id': res_partner_id[0]['id'],
                'deduction_point': punti,
                'notes': note,
                'state': "done",
            })
            PRINT("Creazione eseguita")
        
#     # Verifico se il brand, il modello e la targa sono già inseriti nel db
#     is_targa = COCOZZA_connectDb.sqlSearch('fleet.vehicle', ['name', '=', targa])
#     is_cdc = COCOZZA_connectDb.sqlSearch('res.partner', ['name', '=', cdc])
    
#     # print("FACCIO UN POO' DI PRINT")
#     # print(is_brand)
#     # print(is_modello)
#     # print(is_categoria)
#     # print(is_targa)
#     # print(is_cdc)

#     if targa == None:
#         break

#     # Verifico se la targa è già inserita
#     PRINT("Controllo se la targa è inserita")
#     controllo_targa = COCOZZA_connectDb.sqlSearch('fleet.vehicle',['license_plate', '=', targa])
#     print(controllo_targa)
#     if controllo_targa == []:
#         print("Entro nella if inerente al veicolo non esistente")
#         PRINT(f"La targa {targa} non è esistente.")
#         # Verifico se il brand esiste
#         is_brand = COCOZZA_connectDb.sqlSearch('fleet.vehicle.model.brand', ['name', '=', brand.lower().capitalize()])
#         if is_brand == []:
#             PRINT(f"il Brand {brand} non esiste. Procedo con la creazione.")
#             is_brand = COCOZZA_connectDb.sqlCreate('fleet.vehicle.model.brand',{'name', '=', brand.lower().capitalize()})
#             PRINT(f"Brand creato.")
#         PRINT("Stampo is-brand")
#         PRINT(is_brand)
#         PRINT("Verifica del brand terminata")
        
#         # Verifico se la categoria esiste
#         is_categoria = COCOZZA_connectDb.sqlSearch('fleet.vehicle.model.category', ['name', '=', categoria.lower().capitalize()])
#         if is_categoria == []:
#             PRINT(f"La categoria {categoria} non esiste. Procedo con la creazione della categoria.")
#             is_categoria = COCOZZA_connectDb.sqlCreate('fleet.vehicle.model.category', {'name': categoria.lower().capitalize()})
#             PRINT(f"Categoria {categoria} creata con successo")
#         PRINT("Stampo is-categoria")
#         PRINT(is_categoria)
#         PRINT("Verifica della categoria terminata")

#         # Verifico che il modello esista
#         is_modello = COCOZZA_connectDb.sqlSearchMultiple('fleet.vehicle.model', [('name', '=', modello.lower().capitalize()), ('category_id', '=', is_categoria[0]['id']),('brand_id', '=', is_brand[0]['id'])],{'fields': ['id'], 'limit': 1})
#         print(f"Stampo modello      : {is_modello}")
#         if is_modello == []:
#             PRINT(f"Il modello {modello} non esiste. Procedo con la creazione del modello.")
#             is_modello = COCOZZA_connectDb.sqlCreate('fleet.vehicle.model', {'name': modello.lower().capitalize(),
#                                                                 'brand_id': is_brand[0]['id'],
#                                                                 'category_id': is_categoria[0]['id']})
#             modello_id = is_modello[0]
#             PRINT("Modello creato correttamente con id")
#         else:
#             modello_id = is_modello[0]['id']
#         print("CI PROVOO")
#         PRINT('Stampo is_modello')
#         PRINT(is_modello)
#         PRINT('Stampo modello_id')
#         PRINT(modello_id)
#         PRINT("Verifica del modello terminata")

#         # Creo il mezzo
#         PRINT(f"Procedo con la creazione del veicolo con targa {targa}")
#         print(f"Ecco is_brand = {is_brand[0]['id']}")
#         print(f"Ecco targa = {targa}")
#         print(f"Ecco id_cdc = {is_cdc[0]['id']}")
#         print(f"Ecco modello_id = {modello_id}")
#         COCOZZA_connectDb.sqlCreate("fleet.vehicle", {
#                                                     'brand_id': is_brand[0]['id'],
#                                                     'license_plate': targa,
#                                                     'organization_id': is_cdc[0]['id'],
#                                                     'model_id': modello_id,
#                                                     'euro': euro,
#                                                     'state_vehicle': stato
#                                                     })
#         PRINT("Veicolo aggiunto!")
    
#     else:
#         PRINT(f"Veicolo con targa {targa} già esistente.")
# PRINT("L'IMPORTAZIONE E' FINALMENTE TERMINATA!!!")