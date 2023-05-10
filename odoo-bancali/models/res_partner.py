from odoo import fields, models, api
import datetime

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    bancali_ids = fields.One2many("bancali", "azienda_id")
    bancale_count = fields.Integer(compute='compute_bancale_count')

    def compute_bancale_count(self):
        for record in self:
            record.bancale_count = sum(self.env['bancali'].search(
                [('azienda_id', '=', self.id)]).mapped('differenza'))


    def get_bancali(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bancali',
            'view_mode': 'tree,form',
            'res_model': 'bancali',
            'domain': [('azienda_id', '=', self.id)],
            'context': "{'create': True, 'edit': True}",
        }
