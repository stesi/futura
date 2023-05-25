import xmlrpc.client

# Parametri di connessione al server Odoo
url = 'http://localhost:8069'
db = 'Odoodb16'
username = 'luca.cocozza@futurasl.com'
password = 'Temp1234'

# creazione del client XML-RPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# creazione del nuovo record hr.employee
new_employee = {
                'name': "Nome Cognome aa",
                'first_name': "TEST",
                'last_name': "TEST",
                'l10n_it_codice_fiscale': "MRTMTT91D08F205J",
}

employee_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [new_employee])

print("Nuovo record creato con ID:", employee_id)
