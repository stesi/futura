import json

with open('object.txt') as f:
    data = json.load(f)

codici_fiscali = set()

for record in data:
    if record['Abilitato'] == True:
        codice_fiscale = record['DipCodFiscale']
        if codice_fiscale in codici_fiscali:
            print('Trovato codice fiscale duplicato:', codice_fiscale)
        else:
            codici_fiscali.add(codice_fiscale)
