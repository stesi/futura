{
    'name': 'dipendenti',
    'version': '0.2',
    'author': "Luca Cocozza",
    'application': True,
    'depends': ['hr', 'fleet'],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view,
        'view/hr_update.xml',
    ],
}
