from odoo import fields, models

class Reclami(models.Model):
    _name = "fleet.reclami"
    _description = "Tipologie di reclami"

    name = fields.Char()


class AnomalieUpdate(models.Model):
    _inherit = "fleet.vehicle.log.services"

    reclami = fields.Many2one('fleet.reclami')
