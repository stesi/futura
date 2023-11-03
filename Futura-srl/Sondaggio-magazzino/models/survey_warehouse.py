from odoo import fields, models, api


class WarehousePicking(models.Model):
    _inherit = 'stock.picking'

    

class SurveyWarehouse(models.Model):
    _inherit = 'survey.user_input'
    
    picking_id = fields.One2Many('stock.picking')