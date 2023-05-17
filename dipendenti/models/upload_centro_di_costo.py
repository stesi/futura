import xmlrpc.client
import ssl

# Parametri di connessione
url = 'https://futurasl-test-import-anomalie3-8290237.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8290237'
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
centri_di_costo_data = [    
        {'name': 'CENTINATO'},
        {'name': 'ISOTERMICO'},
        {'name': 'FRIGO MULETTO'},
        {'name': 'TRASPORTO PERSONE'},
        {'name': 'FRIGO'},
        {'name': 'EUROCARGO'},
        {'name': 'CDC'},
        {'name': 'PABL'},
        {'name': 'FECE'},
        {'name': 'FEPD'},
        {'name': 'COBO'},
        {'name': 'COPD'},
        {'name': 'CORM'},
        {'name': 'GETR'},
        {'name': 'PAMO'},
        {'name': 'GENE'},
        {'name': 'COMI'},
        {'name': 'ROCO'},
        {'name': 'PATV'},
        ]

# Creazione delle aziende in Odoo
for centro_di_costo_data in centri_di_costo_data:
    # Cerca se esiste già un record con lo stesso nome
    centro_di_costo_count = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_count',
        [[['name', '=', centro_di_costo_data['name']],
          ['is_company', '=', False],
          ['type', '=', 'delivery']
          ]]
    )
    # Se il conteggio è uguale a zero, crea un nuovo record
    if centro_di_costo_count == 0:
        centro_di_costo_id = models.execute_kw(
            db, uid, password,
            'res.partner', 'create',
            [{'name': centro_di_costo_data['name'],
              'is_company': False,
              'type': 'delivery'}]
        )
        print(f"Creato centro di costo '{centro_di_costo_data['name']}' con ID: {centro_di_costo_id}")
    else:
        print(f"Il centro di costo '{centro_di_costo_data['name']}' esiste già")
