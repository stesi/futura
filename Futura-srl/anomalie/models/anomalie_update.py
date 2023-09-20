from odoo import fields, models

class Reclami(models.Model):
    _name = "fleet.reclami"
    _description = "Tipologie di reclami"

    name = fields.Char()



class AnomalieUpdate(models.Model):
    _inherit = "fleet.vehicle.log.services"

    reclami_selection = fields.Selection([
        ("autista", "Dall'autista"),
        ('fornitore', 'Dal fornitore'),
        ('cliente', 'Dal cliente'),
        ('rop', 'Dal rop'),
        ], 'Reclamo', default="autista")

    reclami_type_id = fields.Many2one('fleet.reclami', 'Tipo di reclamo')
