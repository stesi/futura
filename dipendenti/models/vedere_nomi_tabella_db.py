import xmlrpc.client, ssl

# Connessione al server Odoo
url = 'https://futurasl-test-import-anomalie3-8235343.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8235343'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url),context=context)
uid = common.authenticate(db, username, password, {})

# Oggetto client Odoo
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),context=context)

# Metodo per ottenere i nomi dei campi della tabella res.partner
partner_fields = models.execute_kw(db, uid, password,
    'fleet.vehicle', 'fields_get',[])

# Stampa dei nomi dei campi
for field_name, field_value in partner_fields.items():
    print(field_name)
    # if "Id" in field_name:
    #     print("ABBIAMO TROVATO IL CAMPO")
    #     break
