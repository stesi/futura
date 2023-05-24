{
    'name': 'dipendenti',
    'version': '0.2',
    'author': "Luca Cocozza",
    'application': True,
    'depends': ['hr', 'fleet', 'fleet_replacement', 'fleet_service_with_deduction' ],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view,
        # 'view/hr_update.xml',
        'view/fleet_vehicle_update.xml',
        'view/hr_employee_update.xml'
    ],
}
