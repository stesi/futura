import xmlrpc.client
import ssl

# Parametri di connessione
url = 'https://futurasl-test-import-anomalie3-8356499.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8356499'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()


# Connessione al server Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
uid = common.authenticate(db, username, password, {})

# Creazione di un oggetto per eseguire le operazioni CRUD
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

# Definizione dei dati delle aziende
productors_data = [
    {'name': 'IVECO'},
    {'name': 'DAIMLER'},
    {'name': 'VOLVO'},
    {'name': 'MERCEDES'},
    {'name': 'OPEL'},
    {'name': 'RENAULT'},
    {'name': 'FIAT'},
    {'name': 'KIA'},
    {'name': 'MASTER'},
    {'name': 'ISUZU'},
    {'name': 'MAN'},
    {'name': 'Sconosciuto'}
    ]

# Creazione delle aziende in Odoo
for productor_data in productors_data:
    # Cerca se esiste già un record con lo stesso nome
    productor_count = models.execute_kw(
        db, uid, password,
        'fleet.vehicle.model.brand', 'search_count',
        [[['name', 'like', productor_data['name'].title()]]]
    )
    # Se il conteggio è uguale a zero, crea un nuovo record
    if productor_count == 0:
        productor_id = models.execute_kw(
            db, uid, password,
            'fleet.vehicle.model.brand', 'create',
            [{'name': productor_data['name'].title()}]
        )
        print("Creata produttore con ID:", productor_id)
    else:
        print("Il produttore", productor_data['name'], "esiste già")

