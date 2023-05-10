# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bancali',
    'version': '0.5',
    'author': "Luca Cocozza",
    'application': True,
    'depends': ['contacts'],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view
        'view/bancali_tipologia_views.xml',
        'view/bancali_views.xml',
        'view/bancali_buono_views.xml',
        'view/bancali_deposito_views.xml',
        'view/bancali_fatturazione_views.xml',
        'view/res_partner_view.xml',
        'view/delete_wizard.xml',
        # # Azioni automatizzate
        # 'view/ir_cron_data.xml',        
        # # Caricamento del menu
        'view/bancali_menus.xml',
    ]
}