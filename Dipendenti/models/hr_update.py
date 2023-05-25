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
    interinale = fields.Many2one('hr.interinale')

class ResPartnerUpdate(models.Model):
    _inherit = "res.partner"
    
    first_name = fields.Char()
    last_name = fields.Char()
    

class PworkSetting(models.Model):
    _name = "pwork.setting"
    _description = "Pwork setting"
    
    token = fields.Char()
    
class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"
    
    stato_veicolo = fields.Selection([('ATTIVO', 'ATTIVO'),('IN ARRIVO', 'IN ARRIVO'),('INCIDENTATO','INCIDENTATO'),('RESTITUITO','RESTITUITO')], default="ATTIVO")
    euro = fields.Char()
    
class HrInterinale(models.Model):
    _name = "hr.interinale"
    _description = "Dipendenti interinali"
    
    name = fields.Char(string="Nome azienda interinale")
    res_partner_id = fields.Many2one('res.partner', string="Contatto azienda interinale")
    res_company_id = fields.Many2one('res.company', string="Azienda interna collegata")