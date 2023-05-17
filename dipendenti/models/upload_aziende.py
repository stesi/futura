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

# Creazione di un oggetto per eseguire le operazioni CRUD
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

# Definizione dei dati delle aziende
companies_data = [
    {'name': 'Fresh Archimede'},
    {'name': 'Fresh Areajob Spa'},
    {'name': 'Fresh AXL'},
    {'name': 'Fresh During Spa'},
    {'name': 'Fresh G Group'},
    {'name': 'Fresh Humangest Spa'},
    {'name': 'Fresh Logistics S.r.l.'},
    {'name': 'Fresh MAV'},
    {'name': 'Futura Archimede'},
    {'name': 'Futura Areajob'},
    {'name': 'Futura During'},
    {'name': 'Futura Etjca'},
    {'name': 'Futura Gi Group'},
    {'name': 'Futura MAW'},
    {'name': 'Futura s.r.l.'},
    {'name': 'Futura Tempi Moderni'},
    {'name': 'Holding During'},
    {'name': 'Holding s.r.l.'},
    {'name': 'Logistica During'},
    {'name': 'Logistica Etjca'},
    {'name': 'Logistica Gi Group'},
    {'name': 'Logistica Humangest Spa'},
    {'name': 'Logistica MAW'},
    {'name': 'Logistica s.r.l.'},
    {'name': 'TEST'}
]

# Creazione delle aziende in Odoo
for company_data in companies_data:
    company_id = models.execute_kw(
        db, uid, password,
        'res.company', 'create',
        [company_data]
    )
    print("Creata azienda con ID:", company_id)
