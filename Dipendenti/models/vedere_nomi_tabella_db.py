import xmlrpc.client, ssl
import COCOZZA_connectDb

# Connessione al server Odoo
url = 'https://futurasl-test-import-anomalie3-8291901.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8291901'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url),context=context)
uid = common.authenticate(db, username, password, {})

# Oggetto client Odoo
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),context=context)

# # Metodo per ottenere i nomi dei campi della tabella res.partner
# partner_fields = models.execute_kw(db, uid, password,
#     'fleet.vehicle', 'fields_get',[])

# # Stampa dei nomi dei campi
# for field_name, field_value in partner_fields.items():
#     print(field_name)
#     # if "Id" in field_name:
#     #     print("ABBIAMO TROVATO IL CAMPO")
#     #     break








##### PROVO A INSERIRE L'EMPLOYEE_IDS AL RES.PARTNER



test = COCOZZA_connectDb.sqlSearch('res.partner', ['id', '=', 661], [])
# print(test[0])

# # ID del res.partner e del dipendente da associare
# partner_id = 661
# employee_id = 2898

# # Aggiorna il record del partner con il nuovo valore di employee_ids
# COCOZZA_connectDb.models.execute_kw(db, uid, password, 'hr.employee', 'write', [[employee_id], {
#     'work_contact_id': 2719,
#     }])
# print(test[0])
# print("FATTO")

# COCOZZA_connectDb.models.execute_kw(db, uid, password, 'res.partner', 'write', [[2719], {
#     'employee_ids': [2898],
#     }])

COCOZZA_connectDb.models.execute_kw(db, uid, password, 'res.partner', 'write', [[2719], {'employee_ids': [(4, 2898)]}])


test = COCOZZA_connectDb.sqlSearch('res.partner', ['id', '=', 2719], [])
print(test[0])