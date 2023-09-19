{
    'name': 'anomalie',
    'version': '16',
    'author': "Luca Cocozza",
    'application': True,
    'description': "Aggiunge la possibilità di far fare segnalazioni da parte dei Rop e dei clienti",
    'depends': ['fleet', 'gtms_fleet_organization', 'fleet_limited_traffic_zone', 'gtms_fleet_service_with_deduction', 'fleet_replacement',],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view,
        'view/anomalie_update.xml',
        # Menu
        # 'view/menu.xml',
    ],
}
