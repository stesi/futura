import ssl
import xmlrpc.client

# Configurazione della connessione
url = 'https://futurasl-test-import-anomalie-8212813.dev.odoo.com/'
db = 'futurasl-test-import-anomalie-8212813'
username = 'api@api.it'
password = 'Temp1234'

# Disabilita la verifica SSL
context = ssl._create_unverified_context()

# Crea il proxy per la connessione
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)

# Autenticazione
uid = common.authenticate(db, username, password, {})

if uid:
    print('Connessione riuscita con uid:', uid)
else:
    print('Connessione fallita')


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
    company_id = models.execute_kw(db, uid, password,'res.company', 'create',[company_data])
    print("Creata azienda con ID:", company_id)
