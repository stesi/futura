import ssl, xmlrpc.client
from COCOZZA_logs import PRINT

# connessione al server odoo
url = 'https://futurasl-test-import-anomalie3-8356499.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8356499'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)
uid = common.authenticate(db, username, password, {})


def start():
    if uid:
        PRINT("autenticazione avvenuta")
    else:
        PRINT("autenticazione fallita")
        
        
def sqlSearch(table,query,fields=''):
    result = models.execute_kw(db, uid, password, table, 'search_read', [[query]],{'fields': list(fields)})
    return result

def sqlSearchMultiple(table,query,fields=''):
    if fields is None:
        fields = {}
    result = models.execute_kw(db, uid, password, table, 'search_read', 
                            [query], 
                            {'fields': list(fields)})
    return result


def sqlSearchCount(tabella,query):
    models.execute_kw(db, uid, password,tabella, 'search_count',[query])

def sqlCreate(tabella, oggetto):
    result = models.execute_kw(db, uid, password,tabella, 'create',[[oggetto]])
    return result
    

def sqlWrite(tabella,query):
    models.execute_kw(db, uid, password, tabella, 'write', query)
    
    


# dipendenti = sqlSearchMultiple('hr.employee', [('address_home_id', '=', False), ('active', '=', False)], ['id','name','first_name','last_name','pwork_cf'])

# print(dipendenti)
# with open('dipendenti_senza_contatto.txt', 'a') as f:
#         f.write(str(dipendenti))