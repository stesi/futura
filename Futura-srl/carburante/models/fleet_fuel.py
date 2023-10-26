from odoo import fields, models


class FleetFuelType(models.Model):
    _name = "fleet.fuel.type"
    _description = "Tipi di carburante"

    name = fields.Char()


class FleetFuelCompany(models.Model):
    _name = "fleet.fuel.company"
    _description = "Tabella per associare azienda interna con codice azienda carburante"

    name = fields.Char(compute="_compute_name_company")
    company_reference = fields.Char(string="Company Reference")
    company_id = fields.Many2one('res.company')

    def _compute_name_company(self):
        for record in self:
            if record.company_id:
                record.name = record.company_id.name
            else:
                record.name = ''


class FleetFuel(models.Model):
    _name = "fleet.fuel"
    _description = "Tabella rifornimenti mezzi"

    name = fields.Char(compute='_compute_res_partner_id')
    res_partner_id = fields.Many2one('res.partner', string='Partner', domain="[('is_company','=',True)]")
    reference = fields.Char(string='Reference')
    point_sale_code = fields.Char(string='Point Sale Code')
    location = fields.Char(string='Location')
    address = fields.Char(string='Address')
    transaction_datetime = fields.Datetime(string='Transaction Date and Time')
    ticket = fields.Char(string='Ticket')
    km_fleet = fields.Char(string="Km at moment")
    driver_id = fields.Many2one('res.partner', string='Driver', domain="[('is_driver','=',True)]")
    card_number = fields.Char(string='Card Number')
    fleet_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    product_id = fields.Many2one('fleet.fuel.type', string='Fuel Type')
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Price per Unit', digits=(3, 3))
    price = fields.Float(string='Total Price', digits=(3, 3))
    tax = fields.Float(string='Tax', digits=(3, 3))
    business_name_id = fields.Many2one('res.company', string='company reference')
    invoice = fields.Char(string='Invoice')
    invoice_date = fields.Date(string='Invoice Date')
    invoice_discount = fields.Float(string='Invoice Discount', digits=(3, 3))
    tax_rate = fields.Float(string='Tax Rate', digits=(3, 3))
    price_without_tax = fields.Float(string='Price Without Tax', digits=(6, 3))

    def _compute_res_partner_id(self):
        for record in self:
            if record.reference:
                record.name = record.reference
            else:
                record.name = ''


class FleetFieldsUpdate(models.Model):
    _inherit = "fleet.vehicle"

    capacity_vehicle = fields.Integer(string="Capacity")
    license_request = fields.Selection([('M', 'M'), ('A', 'A'), ('B1', 'B1'), ('B', 'B'), ('C1', 'C1'), ('C', 'C'), ('D1', 'D1'), ('D', 'D'), ('BE', 'BE'), ('C1E', 'C1E'), ('CE', 'CE'), ('D1E', 'D1E'), ('DE', 'DE'), ('T', 'T'), ('F', 'F')])
    euro = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')])


    def open_vehicle_fuel_records(self):
        return {
            'name': 'Rifornimenti del Veicolo',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.fuel',
            'view_mode': 'tree',
            'domain': [('fleet_id', '=', self.id)],
            'context': {
                'default_vehicle_id': self.id,
            },
            'target': 'current',
        }

