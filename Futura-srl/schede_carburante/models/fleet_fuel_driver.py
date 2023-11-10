from odoo import fields, models, api


class FleetFuelDriver(models.Model):
    _name = "fleet.fuel.driver"
    _description = "Tabella storico carte carburanti"


    driver_code = fields.Char()
    driver_pin = fields.Char()
    start_datetime = fields.Datetime()
    end_datetime = fields.Datetime()
    state = fields.Selection(string='Status', required=True, readonly=True, copy=False, selection=[('valid', 'Valida'),('unvalid', 'Non valida'),], default='valid')
    vehicle_id = fields.One2many('fleet.vehicle')



class FleetFieldsUpdate(models.Model):
    _inherit = "res.partner"


    driver_code = fields.Char()
    driver_pin = fields.Char()



    @api.onchange('driver_code', 'driver_pin')
    def _update_fleet_fuel_driver(self):
        self.env['fleet.fuel.driver'].create({
            'driver_code': self.driver_code,
            'driver_pin': self.driver_pin,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
        })
