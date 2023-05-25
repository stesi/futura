import json

# Apri il file in modalità lettura
with open('file.txt', 'r') as file:
    # Leggi il contenuto del file come una stringa JSON e convertilo in un dizionario
    data = json.loads(file.read())

# Inizializza una lista vuota per contenere le informazioni che ti interessano
info_list = []

# Itera su ciascun oggetto nel dizionario e estrai i dati che ti interessano
for item in data:
    info = {
        'nome': item['Nome'],
        'cognome': item['Cognome'],
        'codice_fiscale': item['DipCodFiscale']
    }
    info_list.append(info)

# Stampa la lista di informazioni
print(info_list)
