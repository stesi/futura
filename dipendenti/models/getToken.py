import xmlrpc.client
import requests, logging
import xml.etree.ElementTree as ET
import json ,ssl
import COCOZZA_connectDb
from datetime import datetime, timedelta

context = ssl._create_unverified_context()

COCOZZA_connectDb.start()
datetime_token = COCOZZA_connectDb.sqlSearch('pwork.setting', ['id', '=', 1])
print(datetime_token[0]['__last_update'])
data_datetime = datetime.strptime(datetime_token[0]['__last_update'], "%Y-%m-%d %H:%M:%S")
data_attuale = datetime.now()
differenza = data_attuale - data_datetime
if differenza >= timedelta(hours=24):
    print("Sono passate 24 ore")
else:
    print("Non sono ancora passate 24 ore")


quit()

_logger = logging.getLogger(__name__)


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
TOKEN = data['Generics']['UID']
azienda = data['Generics']['Azienda']
email = data['Generics']['Email']
livello = data['Generics']['Livello']
nome = data['Generics']['Nome']
data_scadenza = data['Generics']['DataScad']
data_scadenza_privacy = data['Generics']['DataScadPrivacy']
data_ultimo_upd = data['Generics']['DataUltimoUpd']
gruppo_user = data['Generics']['GruppoUser']
key_public = data['Generics']['KeyPublic']

print("TOKEN: " + TOKEN)
print("azienda: " + azienda)
print("email: " + email)
print("livello: " + str(livello))
print("nome: " + nome)
print("data scadenza: " + data_scadenza)
print("data scadenza privacy: " + data_scadenza_privacy)
print("data ultimo upd: " + data_ultimo_upd)
print("gruppo user: " + gruppo_user)
print("Key public: " + key_public)

# parametri per la connessione all'istanza di Odoo
url = 'https://futurasl-test-import-anomalie3-8253177.dev.odoo.com/'
db = 'futurasl-test-import-anomalie3-8253177'
username = 'api@api.it'
password = 'Temp1234'

# stabilisci la connessione all'istanza di Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
uid = common.authenticate(db, username, password, {})

_logger.info("Connessione all'istanza di Odoo stabilita con successo")
print("Connessione all'istanza di Odoo stabilita con successo")

# ottieni un oggetto per l'accesso ai metodi del modello "pwork.setting"
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=context)
model_name = 'pwork.setting'

_logger.info("Oggetto per l'accesso ai metodi del modello 'pwork.setting' ottenuto con successo")
print("Oggetto per l'accesso ai metodi del modello 'pwork.setting' ottenuto con successo")

# crea un nuovo record nel modello "pwork.setting"
new_record = {
    'token': TOKEN
}
record_id = models.execute_kw(db, uid, password, model_name, 'create', [new_record])

_logger.info("Record creato con ID: %s", record_id)
print("Record creato con ID: %s", record_id)