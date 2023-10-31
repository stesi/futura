from odoo import fields, models, api


class Diritti(models.Model):
    _inherit = 'fleet.vehicle.log.services'


    groups_ids = fields.Many2many('res.groups', string='Groups of the User')
    is_rop = fields.Boolean(default=False, compute='_compute_is_rop')

    @api.depends('groups_ids')
    def _compute_is_rop(self):
        for record in self:
            record.is_rop = 116 in record.groups_ids.ids