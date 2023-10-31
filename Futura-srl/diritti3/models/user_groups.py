from odoo import fields, models, api


class Diritti(models.Model):
    _inherit = 'fleet.vehicle.log.services'


    groups_ids = fields.Char(string='Groups of the User', compute='_compute_user_groups')
    is_rop = fields.Boolean(compute='_compute_is_rop')

    @api.depends()
    def _compute_user_groups(self):
        for record in self:
            # Trova l'utente connesso
            user = self.env.user
            # Ottieni gli identificatori dei gruppi dell'utente connesso
            record.groups_ids = user.groups_id.ids
            if 116 in record.groups_ids:
                record.is_rop = True

    @api.depends('groups_ids')
    def _compute_is_rop(self):
        for record in self:
            if 116 in record.groups_ids:
                record.is_rop = True