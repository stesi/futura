{
    'name': 'diritti',
    'version': '16',
    'author': "Luca Cocozza",
    'application': False,
    'description': "Aggiunta del campo groups_ids da poter integrare nei moduli.",
    'depends': [],
    'data': [
        # # Settaggi per accesso ai contenuti
        #'data/ir.model.access.csv',
        # # Caricamento delle view,
        'view/groups_field.xml',
    ],
}
