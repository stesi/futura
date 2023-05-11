from odoo import fields, models


class ImportData(models.Model):
    _name = "import.data"
    _description = "Importazione dati"
    
    number_data_import = fields.Integer()

class HrUpdate(models.Model):
    _inherit = "hr.employee"
    
    pwork_cf = fields.Char()
    pwork_azienda_id = fields.Integer()
    pwork_dipendente_id = fields.Integer()
    first_name = fields.Char()
    last_name = fields.Char()

class ResPartnerUpdate(models.Model):
    _inherit = "res.partner"
    
    first_name = fields.Char()
    last_name = fields.Char()
    

class PworkSetting(models.Model):
    _name = "pwork.setting"
    _description = "Pwork setting"
    
    token = fields.Char()
    
