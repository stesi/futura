import xmlrpc.client
import requests
import xml.etree.ElementTree as ET
import json, ssl
from codicefiscale import isvalid
from datetime import datetime



USERNAME = "futuraWS"
PASSWORD = "HGDJSA47432MS"
IP = "127.000.000.001"
SESSION = "Session_0001"
CODAZIENDA = "0020050016"



print("Avvio connessione")

url = 'https://futura.presenze-online.it/webservice/ws.asmx'
headers = {
    'Content-Type': 'application/soap+xml; charset=utf-8',
}

# costruzione del payload della richiesta SOAP XML
payload = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <getToken xmlns="https://presenze-online.it/">
            <Params>
                <Username>{}</Username>
                <Password>{}</Password>
                <Ip>{}</Ip>
                <Session>{}</Session>
                <CodAzienda>{}</CodAzienda>
                <NumHHScadToken>4</NumHHScadToken>
            </Params>
            <ReturnType>FormatJson</ReturnType>
        </getToken>
    </soap12:Body>
</soap12:Envelope>'''.format(USERNAME, PASSWORD, IP, SESSION, CODAZIENDA)

print("Invio della richiesta HTTP POST")

# Invio della richiesta HTTP POST
response = requests.post(url, headers=headers, data=payload)


print("Stampa dello stato della risposta HTTP e del contenuto della risposta")

# stampa dello stato della risposta HTTP e del contenuto della risposta
print(response.status_code)
print(response.content)


# Analisi del documento XML
xml_string = response.content
root = ET.fromstring(xml_string)

# Recupero del valore della stringa JSON
result = root.find('.//{https://presenze-online.it/}getTokenResult').text.strip()

# Analisi della stringa JSON
data = json.loads(result)

# Recupero dei valori desiderati dal dizionario
uid = data['Generics']['UID']
azienda = data['Generics']['Azienda']
email = data['Generics']['Email']
livello = data['Generics']['Livello']
nome = data['Generics']['Nome']
data_scadenza = data['Generics']['DataScad']
data_scadenza_privacy = data['Generics']['DataScadPrivacy']
data_ultimo_upd = data['Generics']['DataUltimoUpd']
gruppo_user = data['Generics']['GruppoUser']
key_public = data['Generics']['KeyPublic']

print("Uid: " + uid)
print("azienda: " + azienda)
print("email: " + email)
print("livello: " + str(livello))
print("nome: " + nome)
print("data scadenza: " + data_scadenza)
print("data scadenza privacy: " + data_scadenza_privacy)
print("data ultimo upd: " + data_ultimo_upd)
print("gruppo user: " + gruppo_user)
print("Key public: " + key_public)


payload = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <getListDipendenti xmlns="https://presenze-online.it/">
            <Token>{}</Token>
            <CodAzienda>{}</CodAzienda>
            <ReturnType>FormatJson</ReturnType>
        </getListDipendenti>
    </soap12:Body>
</soap12:Envelope>'''.format(uid, CODAZIENDA)

print("Invio della richiesta HTTP POST")

# Invio della richiesta HTTP POST
response = requests.post(url, headers=headers, data=payload)


print("Stampa dello stato della risposta HTTP e del contenuto della risposta")

# # stampa dello stato della risposta HTTP e del contenuto della risposta
# print(response.status_code)
# print(response.content)


root = ET.fromstring(response.content)

ns = {'p': 'https://presenze-online.it/'}
result = root.find('.//p:getListDipendentiResult', namespaces=ns).text.strip()


# print(result)

# connessione al server odoo
url = 'https://futurasl-test-import-anomalie3-8232542.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8232542'
username = 'api@api.it'
password = 'Temp1234'
context = ssl._create_unverified_context()


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)


uid = common.authenticate(db, username, password, {})

if uid:
    print("autenticazione avvenuta")
else:
    print("autenticazione fallita")


stringa_corretta1 = result.replace('false', 'False')
stringa_corretta2 = stringa_corretta1.replace('true', 'True')

context = ssl._create_unverified_context()


# stabilisci la connessione all'istanza di Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)

uid = common.authenticate(db, username, password, {})

print("Connessione all'istanza di Odoo stabilita con successo")

cf = ['BDAHBB87M09Z352X','SDAZKR88825Z200D','DNGGRL99L22182V', 'LAFWQS94E08Z236O','GPKPRC86C12Z306Z','MRTMTT91D08F205J','SCRNHT99C10Z140X']




object = eval(stringa_corretta2)


with open('object.txt', 'a') as f:
    f.write(json.dumps(object['Generics']))


#########

for record in object['Generics']:
    azienda_id = models.execute_kw(db, uid, password, 'res.company', 'search', [[('name', '=', record['Azienda'])]])
    azienda_id = azienda_id[0]
    print('Questo è azienda_ID:')
    print(azienda_id)
    print(record)
    if record['Abilitato'] == True:
        # se è attivo
        controllo_cf = models.execute_kw(db, uid, password, 'res.partner', 'search', [[('l10n_it_codice_fiscale', '=', record['DipCodFiscale'])]])
        if controllo_cf == []:
            # se il cf non è presente verifico che sia valido
            if isvalid(record['DipCodFiscale']):
                if not record['DipCodFiscale'] in cf:
                    name = record['Nome'] + " " + record['Cognome']
                    print("Codice fiscale non trovato.\nProcedo con la creasione del res.partner")
                    res_partner_data = {
                        'name': name,
                        'first_name': record['Nome'],
                        'last_name': record['Cognome'],
                        'active': record['Abilitato'],
                        'l10n_it_codice_fiscale': record['DipCodFiscale'],
                    }
                    print("Creazione res.partner eseguita.\nProcedo con la creazione del record in hr.employee")
                    res_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [res_partner_data])
                    print("res_partner_id = " + str(res_partner_id))
                    if record['DipSesso'] == "M":
                        sesso = "male"
                    elif record['DipSesso'] == "F":
                        sesso = "female"
                    else:
                        sesso = ''
                    if 'DipDataNascita' in record:
                        data = datetime.strptime(record['DipDataNascita'], '%Y-%m-%dT%H:%M:%S')
                        data2 = data.date().strftime('%Y-%m-%d')
                    else:
                        data2 = '1900-01-01'
                    print("DATA = ", data2)
                    hr_employ_data = {
                        'name': record['Nome'] + " " + record['Cognome'],
                        'first_name': record['Nome'],
                        'last_name': record['Cognome'],
                        'pwork_cf': record['DipCodFiscale'],
                        'pwork_azienda_id': record['idAz'],
                        'pwork_dipendente_id': record['idDip'],
                        'active': record['Abilitato'],
                        'gender': sesso,
                        'birthday': data2,
                        'company_id': azienda_id,
                        #'res_partner_id': res_partner_id,
                    }
                    employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [hr_employ_data])
                    print("Creazione record in hr.employee eseguita")
                    models.execute_kw(db, uid, password, 'hr.employee', 'write', [[employee_id], {'address_home_id': res_partner_id}])
                    print("Appena associato employee id = " + str(employee_id) + " al contatto id = " + str(res_partner_id))
                else:
                    print("codice fiscale presente nella lista nera")
                    with open('saltati.txt', 'a') as f:
                        f.write(json.dumps(record)+",")
            else:
                print("il codice fiscale non è corretto")
                with open('saltati.txt', 'a') as f:
                    f.write(json.dumps(record)+",")
        else:
            print("Codice fiscale presente in res.partner")
            with open('saltati.txt', 'a') as f:
                f.write(json.dumps(record)+",")
    else:
        print("Utente NON attivo")
        print("Controllo se il dipendente è già inserito trai dipendenti.")
        employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip'])]])
        if employee_ids == []:
            print("Dipendente non inserito...")
            if record['DipSesso'] == "M":
                sesso = "male"
            elif record['DipSesso'] == "F":
                sesso = "female"
            else:
                sesso = ''
            if 'DipDataNascita' in record:
                data = datetime.strptime(record['DipDataNascita'], '%Y-%m-%dT%H:%M:%S')
                data2 = data.date().strftime('%Y-%m-%d')
            else:
                data2 = '1900-01-01'
            print("DATA = ", data2)
            hr_employ_data = {
                        'name': record['Nome'] + " " + record['Cognome'],
                        'first_name': record['Nome'],
                        'last_name': record['Cognome'],
                        'pwork_cf': record['DipCodFiscale'],
                        'pwork_azienda_id': record['idAz'],
                        'pwork_dipendente_id': record['idDip'],
                        'active': record['Abilitato'],
                        'gender': sesso,
                        'birthday': data2,
                        'company_id': azienda_id,
                    }
            models.execute_kw(db, uid, password, 'hr.employee', 'create', [hr_employ_data])
            print("Creazione record in hr.employee eseguita")
        else:
            with open('saltati.txt', 'a') as f:
                f.write(json.dumps(record)+",")

#####



# i = 0
# for record in object['Generics']:
#     i = record['idDip']
#     print("i vale = ", i)
#     if 1 == 1:
#         print(record)
#         if record['Abilitato'] == True:
#             print("L'utente è attivo.\nControllo se il suo codice fiscale è già presente tra i nostri res.partner")
#             controllo_cf = models.execute_kw(db, uid, password, 'res.partner', 'search', [[('l10n_it_codice_fiscale', '=', record['DipCodFiscale'])]])
#             print("controllo cf:")
#             print(controllo_cf)
#             name = record['Nome'] + " " + record['Cognome']
#             if record['DipCodFiscale'] in cf:
#                 print("TROVATO CODICE FISCALE NELLA LISTA CF")
#             if not record['DipCodFiscale'] in cf:
#                 if isvalid(record['DipCodFiscale']):
#                     if controllo_cf == []:
#                         print("Codice fiscale non trovato.\nProcedo con la creasione del res.partner")
#                         res_partner_data = {
#                             'name': name,
#                             'first_name': record['Nome'],
#                             'last_name': record['Cognome'],
#                             'l10n_it_codice_fiscale': record['DipCodFiscale']
#                         }
#                         print("Creazione res.partner eseguita.\nProcedo con la creazione del record in hr.employee")
#                         res_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [res_partner_data])
#                         if record['DipSesso'] == "M":
#                             sesso = "male"
#                         else:
#                             sesso = "female"
#                         if 'DipDataNascita' in record:
#                             data = datetime.strptime(record['DipDataNascita'], '%Y-%m-%dT%H:%M:%S')
#                             data2 = data.date().strftime('%Y-%m-%d')
#                         else:
#                             data2 = '1900-01-01'
#                         print("DATA = ", data2)
#                         hr_employ_data = {
#                             'name': "Nome Cognome aa",
#                             'first_name': record['Nome'],
#                             'last_name': record['Cognome'],
#                             'pwork_cf': record['DipCodFiscale'],
#                             'pwork_azienda_id': record['idAz'],
#                             'pwork_dipendente_id': record['idDip'],
#                             'active': record['Abilitato'],
#                             'gender': sesso,
#                             'birthday': data2,
#                             #'res_partner_id': res_partner_id,
#                         }
#                         models.execute_kw(db, uid, password, 'hr.employee', 'create', [hr_employ_data])
#                         print("Creazione record in contratti.dipendenti eseguita")
#                     else:
#                         print("Utente non abilitato.\nControllo se idAzienda e idDipendente sono già inseriti in hr.employee")
#                         controllo_matricola = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip'])]])
#                         if controllo_matricola == []:
#                             hr_employ_data = {
#                             'name': "Nome Cognome aa",
#                             'first_name': record['Nome'],
#                             'last_name': record['Cognome'],
#                             'pwork_cf': record['DipCodFiscale'],
#                             'pwork_azienda_id': record['idAz'],
#                             'pwork_dipendente_id': record['idDip'],
#                             'active': record['Abilitato'],
#                             }
#                             models.execute_kw(db, uid, password, 'hr.employee', 'create', [hr_employ_data])
#                             print("Ho creato un record nella tabella contratti.dipendenti")
#                         else:
#                             print("Record già registrato in contratti.dipendenti")
#                     with open('file.txt', 'a') as f:
#                         f.write(json.dumps(record)+",")
#                 else:
#                     with open('file.txt', 'a') as f:
#                         f.write(json.dumps(record)+",")

                    
#     #     #     #controllo se3 già inserito in contratti.dipendenti
#     #     #     controllo = common.execute_kw(db, uid, password, 'contratti.dipendenti', 'search', [[('pwork_azienda_id', '=', record['idAzienda']), ('pwork_dipendente_id', '=', record['idDipendente'])]])
#     #     #     if controllo != []:
#     #     #         # se non è presente lo creo
#     #     #         name = record['Nome'] + " " + record['Cognome']
                
#     #     #         set_contratti_dipendenti_data = common.env['contratti.dipendenti'].create(contratti_dipendenti_data)
#     #     #         print("Creazione contratto dipendente eseguita.")

#     #     #     print("Controllo se il dipendente è già inserito trai dipendenti.")
#     #     #     employee_ids = common.execute_kw(db, uid, password, 'hr.employee', 'search', [[('pwork_azienda_id', '=', record['idAzienda']), ('pwork_dipendente_id', '=', record['idDipendente'])]])
#     #     #     if employee_ids == []:
#     #     #         print("L'utente non è presente tra i dipendenti.\nCreo un nuovo dipente.")
#     #     #         name = record['Nome'] + " " + record['Cognome']
#     #     #         employee_data = {
#     #     #             'name': name,
#     #     #             'first_name': record['Nome'],
#     #     #             'last_name': record['Cognome'],
#     #     #             'pwork_cf': record['DipCodFiscale'],
#     #     #             'pwork_azienda_id': record['idAzienda'],
#     #     #             'pwork_dipendente_id': record['idDip'],
#     #     #         }
#     #     #         employee_id = common.env['hr.employee'].create(employee_data)
#     #     #         print("User creato\nControllo se il dipendente è attivo.")
#     #     #         if record['Abilitato'] == True:
#     #     #             print("L'utente è abilitato.\nControllo se l'user è già inserito tramite controllo sul CF")
#     #     #             user_id = common.execute_kw(db, uid, password, 'res.partner', 'search', [[('fiscalcode', '=', record['DipCodFiscale'])]])
#     #     #             if user_ids == []:
#     #     #                 print("Non è associato alcun user.\nProcedo alla creazione dell'user.")
#     #     #                 user_data = {
#     #     #                     'name': name,
#     #     #                     'first_name': record['Nome'],
#     #     #                     'last_name': record['Cognome'],
#     #     #                 }
#     #     #                 common.execute_kw(db, uid, password, 'res.partner', 'create', [user_data])


#     #     # """ # Creazione di un nuovo record nella tabella hr.employee e res.users
#     #     # employee_data = {'name': 'Mario Rossi'}
#     #     # employee_id = odoo.env['hr.employee'].create(employee_data)
#     #     # user_data = {'name': employee_data['name'], 'login': 'mario.rossi', 'password': 'myPassword'}
#     #     # user_id = odoo.env['res.users'].create(user_data)
#     #     # odoo.env['hr.employee'].write(employee_id, {'user_id': user_id})

#     #     # print("Record creato con successo con ID:", employee_id, "e ID utente:", user_id)
#     #     # """