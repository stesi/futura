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
    note = fields.Char()
    consegnati = fields.Integer()
    azienda_id = fields.Many2one("res.partner", domain=[('is_company', '=', True)])
    deposito_id = fields.Many2one("bancali.deposito")
    differenza = fields.Integer(compute="_compute_difference")
    buono_bancali = fields.Binary(attachment=True)
    
    def _compute_difference(self):
        for record in self:
            record.differenza = record.ricevuti - record.consegnati
    
    
    # def create_wizard(self):
    #     wizard = self.env['delete.wizard'].create({
    #         'record_id': self.id,
    #         'record_azienda_id': self.azienda_id,
    #     })
    #     record = self.id
    #     return {
        
    #     'name': 'Eliminazione Record',
        
    #     'type': 'ir.actions.act_window',
        
    #     'res_model': 'delete.wizard',
        
    #     'view_mode': 'form',
        
    #     'res_id': wizard.id,
                
    #     'target': 'new'
    #     }
    
    
    # # Rimuovere determinati Filtri, Group By e possibilità di esportare campi
    # @api.model
    # def fields_get(self, fields=None):
    #     hide = ['id','create_date','write_date','write_uid','create_uid']
    #     res = super(Bancali, self).fields_get()
    #     for field in hide:
    #         res[field]['search'] = False  # To Hide Field From Filter - Odoo >= V15
    #         res[field]['group_operator'] = "false" # To Hide Field From Filter
    #         res[field]['sortable'] = False # To Hide Field From Group by        
    #         res[field]['store'] = False # to hide in 'Select Columns' filter 
    #     return res

        

class Depositi(models.Model):
    _name = 'bancali.deposito'
    _description = 'Deposito bancali'
    
    name = fields.Char()
    code = fields.Char()
    address = fields.Char()
    zip = fields.Integer()
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
        
    def ciao(self):
        _logger.info("CIAO CIAO CIAO CIAO")

        

        
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
        fatturazione_deposito = self.env['bancali.deposito'].search([('name', '=', 'Fatturazione')]).id
        self.env["bancali"].create(
            {
                "data_movimentazione": self.data_movimentazione,
                "tipologia_id": self.tipologia_id.id,
                "azienda_id": self.azienda_id.id,
                "consegnati": self.consegnati,
                "deposito_id": fatturazione_deposito,
                "note": "Bancali fatturati",
            }
        ),
        fatturazione_channel = self.env['mail.channel'].search([('name', '=', 'Fatturazione Bancali')]).id
        consegnati = self.consegnati
        azienda = self.azienda_id.name
        self.env["account.move"].create(
                {
                    "partner_id": self.azienda_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": self.data_movimentazione,
                    "journal_id": 1,
                    "invoice_line_ids": [
                        (0, None, {
                            "name": 'Fatturazione bancali ' + self.tipologia_id.name,
                            "quantity": consegnati,
                            "price_unit": 10, # 10€ costo del singolo bancale
                        },
                        ),
                    ]                  
                }
        ),
        body = "Ho appena creato una bozza per poter fatturare " + str(consegnati) + " bancali al vettore " + azienda
        channel = self.env['mail.channel'].sudo().search([('name', '=', 'Fatturazione')])
        message = self.env['mail.message'].sudo().create({
            'subject': 'Fatturazione bancali',
            'body': body,
            'author_id': self.env.user.partner_id.id,
            'model': None,
            'res_id': None,
            'channel_ids': [(fatturazione_channel)],
        }),
        return { 
                'name': 'Movimentazione Bancali',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'bancali',
                'view_id': self.env.ref('bancali.bancali_views_tree').id,
                'target': 'main',
                'domain': [('azienda_id', '=', self.azienda_id.id)],
            }    
    
    
class DeleteWizard(models.TransientModel):
    _name = 'delete.wizard'
    _description = 'Delete Wizard'
    
    password = fields.Char()
    record_id = fields.Integer()
    record_azienda_id = fields.Integer()
    
    
    def confirm_delete(self):
        if self.password == "ParlaParla":
            my_record = self.env['bancali'].browse(self.record_id)
            my_record.sudo().unlink()
            return {
                'name': 'Movimentazione Bancali',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': 'bancali',
                'view_id': self.env.ref('bancali.bancali_views_tree').id,
                'target': 'main',
                'domain': [('azienda_id', '=', self.record_azienda_id)],
            }         
        else:
            raise ValidationError("Invalid Password")

class ModuleInstaller(models.AbstractModel):
    _name = 'bancali.installer'
    _description = 'Bancali installer'

    @api.model
    def post_upgrade(self, upgraded):
        # Aggiungi un _logger.info statement qui per verificare se la funzione viene effettivamente chiamata
        _logger.info('post_upgrade() chiamata!')
        
        # Controlla se il modulo specificato è stato aggiornato
        if 'bancali-odoo' in upgraded:
            # Aggiungi qui il codice per le operazioni post-upgrade desiderate
            deposito_obj = self.env['bancali_deposito']
            record = deposito_obj.search([('name', '=', 'Fatturazione')])
            
            # Inverti la logica qui e crea un nuovo deposito solo se NON esiste già uno con quel nome
            if not record:
                self.env['bancali.deposito'].create({
                        'name': 'Fatturazione',
                })
                _logger.info('Il deposito "Fatturazione" è stato creato con successo!')
            else:
                _logger.info('Il deposito "Fatturazione" già esiste!')
