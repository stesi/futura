from odoo import models, fields, api
from odoo.exceptions import ValidationError
from werkzeug.utils import redirect

import logging

_logger = logging.getLogger(__name__)

class TipologiaBancali(models.Model):
    _name = 'bancali.tipologia'
    _description = 'Tipologia Bancali'
    
    name = fields.Char()

class Bancali(models.Model):
    _name = 'bancali'
    _description = 'Bancali'
    
    data_movimentazione = fields.Date()
    tipologia_id = fields.Many2one('bancali.tipologia')
    ricevuti = fields.Integer(string="Ritirati")
    consegnati = fields.Integer()
    azienda_id = fields.Many2one("res.partner", domain=[('is_company', '=', True)])
    deposito_id = fields.Many2one("bancali.deposito")
    differenza = fields.Integer(compute="_compute_difference")
    note = fields.Char()
    
    def _compute_difference(self):
        for record in self:
            record.differenza = record.ricevuti - record.consegnati
    
    def create_wizard(self):
        wizard = self.env['delete.wizard'].create({
            'record_id': self.id
        })
        record = self.id
        return {
        
        'name': 'Eliminazione Record',
        
        'type': 'ir.actions.act_window',
        
        'res_model': 'delete.wizard',
        
        'view_mode': 'form',
        
        'res_id': wizard.id,
                
        'target': 'new'
        }
    
    # Rimuovere determinati Filtri, Group By e possibilità di esportare campi
    @api.model
    def fields_get(self, fields=None):
        hide = ['id','create_date','write_date','write_uid','create_uid']
        res = super(Bancali, self).fields_get()
        for field in hide:
            res[field]['searchable'] = False # To Hide Field From Filter - Odoo V14
            res[field]['selectable'] = False # To Hide Field From Filter - Odoo >= V15
            res[field]['sortable'] = False # To Hide Field From Group by        
            res[field]['exportable'] = False # To Hide Field From Export List
            res[field]['store'] = False # to hide in 'Select Columns' filter 
        return res
        

    

    
    
class BuonoBancali(models.Model):
    _name = 'bancali.buono'
    _description = 'Buono bancali'
    
    numero = fields.Char()
    bancali_id = fields.Many2one('bancali')
    file = fields.Binary()
    allegato = fields.Many2many('ir.attachment')
    
    
class Depositi(models.Model):
    _name = 'bancali.deposito'
    _description = 'Deposito bancali'
    
    name = fields.Char()
    code = fields.Char(size=10)
    address = fields.Char()
    zip = fields.Integer(size=5)
    city = fields.Char()
    bancali_ids = fields.One2many("bancali", "deposito_id")
    
    
    bancale_count = fields.Integer(compute='compute_bancale_count')

    def compute_bancale_count(self):
        for record in self:
            record.bancale_count = sum(self.env['bancali'].search(
                [('deposito_id', '=', self.id)]).mapped('differenza'))


    def get_bancali(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bancali',
            'view_mode': 'tree,form',
            'res_model': 'bancali',
            'domain': [('deposito_id', '=', self.id)],
            'context': "{'create': True, 'edit': True}",
        }

    

class DeleteWizard(models.TransientModel):
    _name = 'delete.wizard'
    _description = 'Delete Wizard'
    
    password = fields.Char()
    record_id = fields.Integer()
    
    
    def confirm_delete(self):
        if self.password == "XXX":
            my_record = self.env['bancali'].browse(self.record_id)
            my_record.sudo().unlink()
            return {
                'name': 'Movimentazione Bancali',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'bancali',
                'view_id': self.env.ref('odoo-bancali.bancali_views_tree').id,
                'target': 'main',
            }         
        else:
            raise ValidationError("Invalid Password")

        
class FatturazioneBancali(models.TransientModel):
    _name = 'bancali.fatturazione'
    _description = 'Fatturazione Bancali'
    
    data_movimentazione = fields.Date()
    tipologia_id = fields.Many2one('bancali.tipologia')
    consegnati = fields.Integer()
    azienda_id = fields.Many2one("res.partner", domain=[('is_company', '=', True)])
    deposito_id = fields.Many2one("bancali.deposito")
    note = fields.Char()
    
    
    
    def fatturazione_bancali(self):
        self.env["bancali"].create(
            {
                "data_movimentazione": self.data_movimentazione,
                "tipologia_id": self.tipologia_id.id,
                "azienda_id": self.azienda_id.id,
                "consegnati": self.consegnati,
                "deposito_id": '3',
                "note": "Bancali fatturati",
            }
        ),
        self.env["account.move"].create(
                {
                    "partner_id": self.azienda_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": self.data_movimentazione,
                    "journal_id": 1,
                    "invoice_line_ids": [
                        (0, None, {
                            "name": 'Fatturazione bancali',
                            "quantity": 1,
                            "price_unit": self.consegnati * 10,
                        },
                        ),
                    ]                  
                }
        )
        return {
                'name': 'Movimentazione Bancali',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'bancali',
                'view_id': self.env.ref('odoo-bancali.bancali_views_tree').id,
                'target': 'main',
            }     