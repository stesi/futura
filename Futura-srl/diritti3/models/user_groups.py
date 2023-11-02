from odoo import fields, models, api


class Diritti(models.Model):
    _inherit = 'fleet.vehicle'


    groups_ids = fields.Many2many('res.groups', string='Groups of the User', compute='_compute_groups_ids', store=False)
    is_rop = fields.Boolean(compute='_compute_groups_ids', store=False)

    @api.depends('groups_ids')
    def _compute_groups_ids(self):
        for record in self:
            # Trova l'utente connesso
            user = self.env.user
            # Ottieni gli identificatori dei gruppi dell'utente connesso
            record.groups_ids = user.groups_id.ids
            if 116 in record.groups_ids:
                record.is_rop = True
