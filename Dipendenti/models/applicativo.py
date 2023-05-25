import xmlrpc.client
import requests
import xml.etree.ElementTree as ET
import json, ssl
from codicefiscale import codicefiscale
from datetime import datetime
from COCOZZA_logs import START_LOGS, PRINT
import COCOZZA_connectDb

START_LOGS()

USERNAME = "futuraWS"
PASSWORD = "HGDJSA47432MS"
IP = "127.000.000.001"
SESSION = "Session_0001"
CODAZIENDA = "0020050016"



PRINT("Avvio connessione")

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

PRINT("Invio della richiesta HTTP POST")

# Invio della richiesta HTTP POST
response = requests.post(url, headers=headers, data=payload)


PRINT("Stampa dello stato della risposta HTTP e del contenuto della risposta")

# stampa dello stato della risposta HTTP e del contenuto della risposta
PRINT(response.status_code)
PRINT(response.content)


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

PRINT("Uid: " + uid)
PRINT("azienda: " + azienda)
PRINT("email: " + email)
PRINT("livello: " + str(livello))
PRINT("nome: " + nome)
PRINT("data scadenza: " + data_scadenza)
PRINT("data scadenza privacy: " + data_scadenza_privacy)
PRINT("data ultimo upd: " + data_ultimo_upd)
PRINT("gruppo user: " + gruppo_user)
PRINT("Key public: " + key_public)


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

PRINT("Invio della richiesta HTTP POST")

# Invio della richiesta HTTP POST
response = requests.post(url, headers=headers, data=payload)


PRINT("Stampa dello stato della risposta HTTP e del contenuto della risposta")

# # stampa dello stato della risposta HTTP e del contenuto della risposta
# PRINT(response.status_code)
# PRINT(response.content)


root = ET.fromstring(response.content)

ns = {'p': 'https://presenze-online.it/'}
result = root.find('.//p:getListDipendentiResult', namespaces=ns).text.strip()


# PRINT(result)

# Avvio delle connessione alle api di Odoo
COCOZZA_connectDb.start()

stringa_corretta1 = result.replace('false', 'False')
stringa_corretta2 = stringa_corretta1.replace('true', 'True')






object = eval(stringa_corretta2)


with open('object.txt', 'a') as f:
    f.write(json.dumps(object['Generics']))


#########

i = 0

for record in object['Generics']:
    # Escludo utenti pwork con nome o cognome che contengno la stringa "DUP_"
    if ('Nome' in record and 'DUP_' in record['Nome'].lower()) or ('Cognome' in record and 'DUP_' in record['Cognome'].lower()):
        continue

    # differenzio le aziende Pwork con quelle reali di Futura
    if azienda in ['Fresh Archimede', 'Fresh Areajob Spa', 'Fresh AXL', 'Fresh During Spa', 'Fresh G Group', 'Fresh Humangest Spa', ]
    azienda_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'res.company', 'search', [[('name', '=', record['Azienda'])]])
    azienda_id = azienda_id[0]
    PRINT('Questo è azienda_ID:')
    PRINT(azienda_id)
    PRINT(record)
    if record['Abilitato'] == True:
        # se è attivo
        controllo_cf = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'res.partner', 'search', [[('l10n_it_codice_fiscale', '=', record['DipCodFiscale'])]])
        if controllo_cf == []:
            # se il cf non è presente verifico che sia valido
            if codicefiscale.is_valid(record['DipCodFiscale']):
                name = record['Cognome'] + " " + record['Nome']
                PRINT("Codice fiscale non trovato.\nProcedo con la creasione del res.partner")
                res_partner_data = {
                    'name': name,
                    'first_name': record['Nome'],
                    'last_name': record['Cognome'],
                    'active': record['Abilitato'],
                    'l10n_it_codice_fiscale': record['DipCodFiscale'],
                }
                PRINT("Creazione res.partner eseguita.\nProcedo con la creazione del record in hr.employee")
                res_partner_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'res.partner', 'create', [res_partner_data])
                PRINT("res_partner_id = " + str(res_partner_id))
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
                PRINT(f"DATA = {data2}")
                hr_employ_data = {
                    'name': record['Cognome'] + " " + record['Nome'],
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
                employee_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'create', [hr_employ_data])
                PRINT("Creazione record in hr.employee eseguita")
                COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'write', [[employee_id], {'address_home_id': res_partner_id}])
                PRINT("Appena associato employee id = " + str(employee_id) + " al contatto id = " + str(res_partner_id))
            else:
                PRINT("Il codice fiscale non è corretto.")
                #### CREARE EMPLOYEE PER UTENTI CON CODICE FISCALE ERRATO ###
                # Controllo se il dipendente è  già un hr.employee
                is_employee = COCOZZA_connectDb.sqlSearchMultiple('hr.employee', [('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip'])], '')
                if is_employee != []:
                    PRINT("Il dipendente esiste già in hr.employee")
                    continue
                else:
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
                    PRINT(f"DATA = {data2}")
                    hr_employ_data = {
                        'name': record['Cognome'] + " " + record['Nome'],
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
                    employee_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'create', [hr_employ_data])
                    PRINT("Creazione record in hr.employee eseguita")
                
                with open('res_partner_saltati.txt', 'a') as f:
                    f.write(json.dumps(record)+",")
        else:
            PRINT("Codice fiscale presente in res.partner")
            # Controllo se il dipendente è  già un hr.employee
            is_employee = COCOZZA_connectDb.sqlSearchMultiple('hr.employee', [('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip'])], '')
            if is_employee != []:
                PRINT("Il dipendente esiste già in hr.employee")
                continue
            else:
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
                PRINT(f"DATA = {data2}")
                hr_employ_data = {
                    'name': record['Cognome'] + " " + record['Nome'],
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
                employee_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'create', [hr_employ_data])
                PRINT("Creazione record in hr.employee eseguita")
    else:
        PRINT("Utente NON attivo")
        PRINT("Controllo se il dipendente è già inserito trai dipendenti.")
        employee_ids = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'search', [[('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip']), ('active', 'ilike', False)]])
        if employee_ids == []:
            PRINT("Dipendente non inserito...")
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
            PRINT(f"DATA = {data2}")
            hr_employ_data = {
                        'name': record['Cognome'] + " " + record['Nome'],
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
            employee_id = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'create', [hr_employ_data])
            PRINT("Creazione record in hr.employee eseguita")
            # Controllo se è già stato creato un res.partner e nel caso lo creo
            PRINT("Controllo se esiste il res.partner associabile al dipendente appena creato.")
        

            if codicefiscale.is_valid(record['DipCodFiscale']) == False:
                PRINT("\nCodice fiscale non valido. Salto la creazione del res.partner")
                continue
            cod_fiscale = record['DipCodFiscale'][0:14]
            PRINT(f"codice fiscale {cod_fiscale}")
            res_partner_id = COCOZZA_connectDb.sqlSearchMultiple('res.partner', [('name', 'ilike', record['Cognome'] + " " + record['Nome']),('l10n_it_codice_fiscale', 'ilike', cod_fiscale)])
            if res_partner_id == []:
                res_partner_data = {
                        'name': record['Cognome'] + " " + record['Nome'],
                        'first_name': record['Nome'],
                        'last_name': record['Cognome'],
                        'active': True,
                        'l10n_it_codice_fiscale': record['DipCodFiscale'],
                    }
                PRINT("Creazione res.partner eseguita.\nProcedo con la creazione del record in hr.employee")
                res_partner_id2 = COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'res.partner', 'create', [res_partner_data])
            else:
                res_partner_id2 = res_partner_id[0]['id']
            # Faccio l'associazione del dipendente con il res.partner
            PRINT(f"Stampo employee_id = {employee_id}")
            PRINT(f"Stampo res_partner_id = {res_partner_id2}")
            COCOZZA_connectDb.models.execute_kw(COCOZZA_connectDb.db, COCOZZA_connectDb.uid, COCOZZA_connectDb.password, 'hr.employee', 'write', [[employee_id], {'address_home_id': res_partner_id2}])
            PRINT("Appena associato employee id = " + str(employee_id) + " al contatto id = " + str(res_partner_id2))   
        else:
            PRINT("\nUtente già inserito.")

    