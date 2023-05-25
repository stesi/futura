{
    'name': 'dipendenti',
    'version': '0.2',
    'author': "Luca Cocozza",
    'application': True,
    'depends': ['hr', 'fleet', 'gtms_fleet_organization', 'fleet_limited_traffic_zone', 'gtms_fleet_service_with_deduction', 'fleet_replacement',],
    'data': [
        # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # Caricamento delle view,
        # 'view/hr_update.xml',
        'view/fleet_vehicle_update.xml',
        'view/hr_employee_update.xml',
        'view/hr_interinale_view.xml',
        # Menu
        'view/menu.xml',
    ],
}
