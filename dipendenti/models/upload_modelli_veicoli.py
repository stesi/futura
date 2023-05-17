import xmlrpc.client
import ssl

# Parametri di connessione
url = 'https://futurasl-test-import-anomalie3-8253177.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8253177'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()


# Connessione al server Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
uid = common.authenticate(db, username, password, {})

# Creazione di un oggetto per eseguire le operazioni CRUD
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

# Definizione dei dati dei modelli di veicoli
vehicle_models_data = [
    {'produttore': 'IVECO', 'modello': '110/E18', 'categoria': 'CENTINATO'},
    {'produttore': 'DAIMLER', 'modello': 'Sconosciuto', 'categoria': 'ISOTERMICO'},
    {'produttore': 'VOLVO', 'modello': 'Sconosciuto', 'categoria': 'ISOTERMICO'},
    {'produttore': 'IVECO', 'modello': 'Sconosciuto', 'categoria': 'ISOTERMICO'},
    {'produttore': 'IVECO', 'modello': '75', 'categoria': 'CENTINATO'},
    {'produttore': 'IVECO', 'modello': 'DAILY XL', 'categoria': 'FRIGO MULETTO'},
    {'produttore': 'IVECO', 'modello': 'DAILY', 'categoria': 'FRIGO MULETTO'},
    {'produttore': 'IVECO', 'modello': 'DAILY', 'categoria': 'MULETTO FRIGO'},
    {'produttore': 'MERCEDES', 'modello': 'AG 970', 'categoria': 'CENTINATO'},
    {'produttore': 'IVECO', 'modello': 'DAILY', 'categoria': 'FRIGO MULETTO'},
    {'produttore': 'IVECO', 'modello': '35/E4', 'categoria': 'CENTINATO'},
    {'produttore': 'OPEL', 'modello': 'MOVANO', 'categoria': 'CENTINATO'},
    {'produttore': 'IVECO', 'modello': 'DAILY 65C', 'categoria': 'CENTINATO'},
    {'produttore': 'IVECO', 'modello': '120 EL', 'categoria': 'CENTINATO'},
    {'produttore': 'RENAULT', 'modello': 'CLIO', 'categoria': 'TRASPORTO PERSONE'},
    {'produttore': 'IVECO', 'modello': '35C13', 'categoria': 'CENTINATO'},
    {'produttore': 'FIAT', 'modello': 'DUCATO XL', 'categoria': 'FRIGO'},
    {'produttore': 'FIAT', 'modello': 'TALENTO', 'categoria': 'FRIGO'},
    {'produttore': 'RENAULT', 'modello': 'MASTER', 'categoria': 'FRIGO'},
    {'produttore': 'RENAULT', 'modello': 'MASTER', 'categoria': 'CENTINATO'},
    {'produttore': 'KIA', 'modello': 'CEED', 'categoria': 'TRASPORTO PERSONE'},
    {'produttore': 'MASTER', 'modello': 'RENAULT', 'categoria': 'FRIGO'},
    {'produttore': 'IVECO', 'modello': 'DAILY', 'categoria': 'FRIGO'},
    {'produttore': 'ISUZU', 'modello': 'NIR 87A', 'categoria': 'CENTINATO'},
    {'produttore': 'IVECO', 'modello': 'DAILY NEW', 'categoria': 'FRIGO'},
    {'produttore': 'IVECO', 'modello': 'DAILY', 'categoria': 'FRIGO'},
    {'produttore': 'FIAT', 'modello': '500 XL', 'categoria': 'TRASPORTO PERSONE'},
    {'produttore': 'FIAT', 'modello': 'QUBO', 'categoria': 'TRASPORTO PERSONE'},
    {'produttore': 'IVECO', 'modello': 'DAILY XL', 'categoria': 'FRIGO'},
    {'produttore': 'FIAT', 'modello': 'DUCATO', 'categoria': 'FRIGO'},
    {'produttore': 'FIAT', 'modello': 'DUCATO', 'categoria': 'FRIGO MULETTO'},
    {'produttore': 'IVECO', 'modello': '110', 'categoria': 'CENTINATO'},
    {'produttore': 'MAN', 'modello': 'NUTZFAHR', 'categoria': 'ISOTERMICO'},
    {'produttore': 'Sconosciuto', 'modello': 'Sconosciuto', 'categoria': 'FRIGO'},
    {'produttore': 'IVECO', 'modello': 'LARGE', 'categoria': 'FRIGO MULETTO'},
    {'produttore': 'IVECO', 'modello': 'Sconosciuto', 'categoria': 'EUROCARGO'},
    {'produttore': 'IVECO', 'modello': 'LARGE', 'categoria': 'FRIGO'},
    {'produttore': 'IVECO', 'modello': 'Sconosciuto', 'categoria': 'FRIGO'},
    {'produttore': 'FIAT', 'modello': 'DOBLO\'', 'categoria': 'FRIGO'},
    {'produttore': 'Sconosciuto', 'modello': 'Sconosciuto', 'categoria': 'CENTINATO'}
]

# Recupero degli ID delle categorie
categories_ids = {}
for vehicle_model_data in vehicle_models_data:
    category_name = vehicle_model_data['categoria'].upper()
    if category_name not in categories_ids:
        category_count = models.execute_kw(
            db, uid, password,
            'fleet.vehicle.model.category', 'search_count',
            [[['name', '=ilike', category_name]]]
        )
        if category_count == 0:
            # Se la categoria non esiste, la creo
            category_id = models.execute_kw(
                db, uid, password,
                'fleet.vehicle.model.category', 'create',
                [[{'name': category_name.capitalize()}]]
            )
            categories_ids[category_name] = category_id
        else:
            # Se la categoria esiste, recupero il suo ID
            category_ids = models.execute_kw(
                db, uid, password,
                'fleet.vehicle.model.category', 'search',
                [[['name', '=ilike', category_name]]]
            )
            categories_ids[category_name] = category_ids[0]

# Creazione dei modelli di veicoli in Odoo
for vehicle_model_data in vehicle_models_data:
    # Recupero l'ID del Brand
    brand_name = vehicle_model_data['produttore'].upper()
    brand_id = models.execute_kw(
        db, uid, password,
        'fleet.vehicle.model.brand', 'search',
        [[['name', '=ilike', brand_name]]]
    )[0]

    # Cerca se esiste già un record con lo stesso nome, brand e categoria
    model_count = models.execute_kw(
        db, uid, password,
        'fleet.vehicle.model', 'search_count',
        [[['name', '=ilike', vehicle_model_data['modello']],
        ['brand_id', '=', brand_id],
        ['category_id', '=', category_ids,
        ]]]
    )

    # Se il conteggio è uguale a zero, crea un nuovo record
    if model_count == 0:
        category_id = categories_ids[vehicle_model_data['categoria'].upper()]
        model_id = models.execute_kw(
            db, uid, password,
            'fleet.vehicle.model', 'create',
            [[{'name': vehicle_model_data['modello'],
               'brand_id': brand_id,
               'category_id': category_id}]]
        )
        print(f"Creato modello con ID {model_id}[0]")
    else:
        print(f"Il modello {vehicle_model_data['modello']} del produttore {vehicle_model_data['produttore']} con categoria {vehicle_model_data['categoria']} esiste già")
        print(f"Ho ricercato\nIl modello {vehicle_model_data['modello']} con brand id {brand_id} e con categoria id {category_ids[0]}")
