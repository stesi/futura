{
    'name': 'Sondaggi magazzino',
    'version': '16',
    'author': "Luca Cocozza",
    'application': True,
    'description': "Aggiunta la possibilità di gestire i sondaggi per la merce scaricata nei magazzini",
    'depends': ['fleet','carburante', 'inventory'],
    'data': [
        # # Settaggi per accesso ai contenuti
        #'data/ir.model.access.csv',
        # # Caricamento delle view,
        'view/groups_field.xml',
    ],
}
