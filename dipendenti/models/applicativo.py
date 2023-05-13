import xmlrpc.client
import requests
import xml.etree.ElementTree as ET
import json, ssl
from codicefiscale import isvalid
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


cf = ['BDAHBB87M09Z352X','SDAZKR88825Z200D','DNGGRL99L22182V', 'LAFWQS94E08Z236O','GPKPRC86C12Z306Z','MRTMTT91D08F205J','SCRNHT99C10Z140X']




object = eval(stringa_corretta2)


with open('object.txt', 'a') as f:
    f.write(json.dumps(object['Generics']))


#########

for record in object['Generics']:
    azienda_id = models.execute_kw(db, uid, password, 'res.company', 'search', [[('name', '=', record['Azienda'])]])
    azienda_id = azienda_id[0]
    PRINT('Questo è azienda_ID:')
    PRINT(azienda_id)
    PRINT(record)
    if record['Abilitato'] == True:
        # se è attivo
        controllo_cf = models.execute_kw(db, uid, password, 'res.partner', 'search', [[('l10n_it_codice_fiscale', '=', record['DipCodFiscale'])]])
        if controllo_cf == []:
            # se il cf non è presente verifico che sia valido
            if isvalid(record['DipCodFiscale']):
                if not record['DipCodFiscale'] in cf:
                    name = record['Nome'] + " " + record['Cognome']
                    PRINT("Codice fiscale non trovato.\nProcedo con la creasione del res.partner")
                    res_partner_data = {
                        'name': name,
                        'first_name': record['Nome'],
                        'last_name': record['Cognome'],
                        'active': record['Abilitato'],
                        'l10n_it_codice_fiscale': record['DipCodFiscale'],
                    }
                    PRINT("Creazione res.partner eseguita.\nProcedo con la creazione del record in hr.employee")
                    res_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [res_partner_data])
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
                    PRINT("DATA = ", data2)
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
                    PRINT("Creazione record in hr.employee eseguita")
                    models.execute_kw(db, uid, password, 'hr.employee', 'write', [[employee_id], {'address_home_id': res_partner_id}])
                    PRINT("Appena associato employee id = " + str(employee_id) + " al contatto id = " + str(res_partner_id))
                else:
                    PRINT("codice fiscale presente nella lista nera")
                    with open('saltati.txt', 'a') as f:
                        f.write(json.dumps(record)+",")
            else:
                PRINT("il codice fiscale non è corretto")
                with open('saltati.txt', 'a') as f:
                    f.write(json.dumps(record)+",")
        else:
            PRINT("Codice fiscale presente in res.partner")
            with open('saltati.txt', 'a') as f:
                f.write(json.dumps(record)+",")
    else:
        PRINT("Utente NON attivo")
        PRINT("Controllo se il dipendente è già inserito trai dipendenti.")
        employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[('pwork_azienda_id', '=', record['idAz']), ('pwork_dipendente_id', '=', record['idDip'])]])
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
            PRINT("DATA = ", data2)
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
            PRINT("Creazione record in hr.employee eseguita")
        else:
            with open('saltati.txt', 'a') as f:
                f.write(json.dumps(record)+",")

