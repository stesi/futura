import xmlrpc.client

# connessione al server Odoo
url = "http://localhost:8069"
db = "Odoodb16"
username = "luca.cocozza@futurasl.com"
password = "Temp1234"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# creazione del client per l'API
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# codice fiscale da controllare
cf = "RSSMRA80A01H501F"

try:
    # controllo del codice fiscale
    is_valid = models.execute_kw(db, uid, password,
        'stdnum.it.codice_fiscale', 'is_valid', [cf])
    
    if is_valid:
        print("Il codice fiscale {} è valido".format(cf))
    else:
        print("Il codice fiscale {} non è valido".format(cf))
        
except xmlrpc.client.Fault as e:
    print("Errore XML-RPC: ", e.faultCode, e.faultString)

except xmlrpc.client.ProtocolError as e:
    print("Errore nel protocollo di comunicazione: ", e.errcode, e.errmsg)

except Exception as e:
    print("Errore generico: ", str(e))
