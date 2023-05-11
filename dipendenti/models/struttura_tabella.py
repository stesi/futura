import xmlrpc.client
import ssl

# Parametri di connessione
url = 'https://futurasl-test-import-anomalie-8212813.dev.odoo.com/'
db = 'futurasl-test-import-anomalie-8212813'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()


# Connessione al server Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
uid = common.authenticate(db, username, password, {})

# Creazione di un oggetto per eseguire le operazioni CRUD
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

# Recupero dei campi disponibili nella tabella res.partner
partner_fields = models.execute_kw(
    db, uid, password,
    'res.partner', 'fields_get',
    [], {'attributes': ['string']}
)

# Elenco delle colonne da includere nel CSV
fields = list(partner_fields.keys())

# Intestazione del CSV
print(','.join(fields))

# Recupero dei dati di ogni record e scrittura del CSV
partner_ids = models.execute_kw(
    db, uid, password,
    'res.partner', 'search',
    [[]],
)
for partner_id in partner_ids:
    partner_data = models.execute_kw(
        db, uid, password,
        'res.partner', 'read',
        [partner_id, fields],
    )[0]
    # Conversione dei valori delle colonne in stringhe per il CSV
    partner_csv_values = [str(partner_data[field]) for field in fields]
    print(','.join(partner_csv_values))
