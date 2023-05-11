import xmlrpc.client
import ssl

# Parametri di connessione
url = 'https://futurasl-test-import-anomalie3-8232542.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8232542'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()


# Connessione al server Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
uid = common.authenticate(db, username, password, {})
print("Connessione al server Odoo avvenuta con successo")

# Creazione di un oggetto per eseguire le operazioni CRUD
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

# Definizione dei dati delle aziende
categories_data = [
    {'name': 'CENTINATO'},
    {'name': 'ISOTERMICO'},
    {'name': 'FRIGO MULETTO'},
    {'name': 'TRASPORTO PERSONE'},
    {'name': 'FRIGO'},
    {'name': 'EUROCARGO'},
]

# Creazione delle aziende in Odoo
for category_data in categories_data:
    # Cerca se esiste già un record con lo stesso nome
    category_count = models.execute_kw(
        db, uid, password,
        'fleet.vehicle.model.category', 'search_count',
        [[['name', '=', category_data['name']]]]
    )
    # Se il conteggio è uguale a zero, crea un nuovo record
    if category_count == 0:
        category_id = models.execute_kw(
            db, uid, password,
            'fleet.vehicle.model.category', 'create',
            [{'name': category_data['name'].capitalize()}]
        )
        print(f"Creata categoria '{category_data['name']}' con ID: {category_id}")
    else:
        print(f"La categoria '{category_data['name']}' esiste già")
