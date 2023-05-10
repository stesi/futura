{
    'name': 'bancali',
    'version': '1',
    'author': "Luca Cocozza",
    'application': True,
    'depends': ['contacts', 'account'],
    'category': '4',
    'data': [
        # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # Caricamento delle view
        'view/bancali_tipologia_views.xml',
        'view/bancali_deposito_views.xml',
        'view/bancali_fatturazione_views.xml',
        'view/bancali_views.xml',
        'view/res_partner_view.xml',
        # Caricamento del menu
        'view/bancali_menus.xml',
        #caricamento cron
        'view/cron_first_install.xml',
    ],
}
