from odoo import fields, models, api


class FleetFuelType(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "fleet.fuel.type"
    _description = "Tipi di carburante"

    name = fields.Char(tracking=True)


class FleetFuelCompany(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "fleet.fuel.company"
    _description = "Tabella per associare azienda interna con codice azienda carburante"

    name = fields.Char(compute="_compute_name_company")
    company_reference = fields.Char(string="Company Reference", tracking=True)
    company_id = fields.Many2one('res.company', tracking=True)

    def _compute_name_company(self):
        for record in self:
            if record.company_id:
                record.name = record.company_id.name
            else:
                record.name = ''


class FleetFuel(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "fleet.fuel"
    _description = "Tabella rifornimenti mezzi"

    name = fields.Char(compute='_compute_res_partner_id', readonly=True)
    res_partner_id = fields.Many2one('res.partner', string='Partner', domain="[('is_company','=',True)]", readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    point_sale_code = fields.Char(string='Point Sale Code', readonly=True)
    location = fields.Char(string='Location', readonly=True)
    address = fields.Char(string='Address', readonly=True)
    transaction_datetime = fields.Datetime(string='Transaction Date and Time', readonly=True)
    ticket = fields.Char(string='Ticket', readonly=True)
    km_fleet = fields.Char(string="Km at moment", tracking=True)
    driver_id = fields.Many2one('res.partner', string='Driver', domain="[('is_driver','=',True)]", tracking=True)
    card_number = fields.Char(string='Card Number', readonly=True)
    fleet_id = fields.Many2one('fleet.vehicle', string='Vehicle', tracking=True)
    product_id = fields.Many2one('fleet.fuel.type', string='Fuel Type', readonly=True)
    quantity = fields.Float(string='Quantity', readonly=True)
    price_unit = fields.Float(string='Price per Unit', digits=(3, 3), readonly=True)
    price = fields.Float(string='Total Price', digits=(3, 3), readonly=True)
    tax = fields.Float(string='Tax', digits=(3, 3), readonly=True)
    business_name_id = fields.Many2one('res.company', string='company reference', readonly=True)
    invoice = fields.Char(string='Invoice', readonly=True)
    invoice_date = fields.Date(string='Invoice Date', readonly=True)
    invoice_discount = fields.Float(string='Invoice Discount', digits=(3, 3), readonly=True)
    tax_rate = fields.Float(string='Tax Rate', digits=(3, 3), readonly=True)
    price_without_tax = fields.Float(string='Price Without Tax', digits=(6, 3), readonly=True)
    state = fields.Selection([('da_verificare', 'Da verificare'), ('verificato', 'Verificato'), ('richiesto_rimborso', 'Richiesto rimborso'), ('rimborsato', 'Rimborsato')], tracking=True)

    def _compute_res_partner_id(self):
        for record in self:
            if record.reference:
                record.name = record.reference
            else:
                record.name = ''


class FleetFieldsUpdate(models.Model):
    _inherit = "fleet.vehicle"

    capacity_vehicle = fields.Integer(string="Capacity", tracking=True)
    license_request = fields.Selection([('M', 'M'), ('A', 'A'), ('B1', 'B1'), ('B', 'B'), ('C1', 'C1'), ('C', 'C'), ('D1', 'D1'), ('D', 'D'), ('BE', 'BE'), ('C1E', 'C1E'), ('CE', 'CE'), ('D1E', 'D1E'), ('DE', 'DE'), ('T', 'T'), ('F', 'F')], tracking=True)
    euro = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], tracking=True)

    def open_vehicle_fuel_records(self):
        return {
            'name': 'Rifornimenti del veicolo',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.fuel',
            'view_mode': 'tree,form',
            'domain': [('fleet_id', '=', self.id)],
            'context': {
                'default_vehicle_id': self.id,
            },
            'target': 'current',
        }

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