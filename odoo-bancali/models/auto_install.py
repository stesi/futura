from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
import xmlrpc.client


_logger = logging.getLogger(__name__)


# informazioni di connessione al database Odoo
url = 'http://localhost:8069'
db = 'Odoodb16'
username = 'luca.cocozza@futurasl.com'
password = 'Temp1234'

class BancaliUpdate(models.Model):
    _inherit = 'bancali.deposito'
    
    
    def first_installation_bancali(self):
        import xmlrpc.client

        # connessione al database
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



        # Controlla se esiste un record in bancali_deposito con il nome "Fatturazione"
        record_ids = models.execute_kw(db, uid, password, 'bancali.deposito', 'search', [[('name', '=', 'Fatturazione')]])
        if record_ids:
            _logger.info("Il record con il nome 'Fatturazione' esiste già nella tabella bancali_deposito.")
        else:
            # Se il record non esiste, viene creato
            vals = {'name': 'Fatturazione'}
            new_record_id = models.execute_kw(db, uid, password, 'bancali.deposito', 'create', [vals])
            _logger.info("Creato un nuovo record con il nome 'Fatturazione' nella tabella bancali_deposito.")


        # verifica se esiste già un gruppo con il nome "Pallets"
        _logger.info("Verifico che il gruppo Pallets esiste...")
        existing_group = models.execute_kw(db, uid, password, 'res.groups', 'search', [[('name', '=', 'Pallets')]])
        _logger.info("Ho creato existing_group:")
        _logger.info(existing_group)
        if existing_group:
            _logger.info('Il gruppo "Pallets" esiste già.')
        else:
            _logger.info('Il gruppo "Pallets" non esiste, verrà creato.')

            # crea il gruppo "Pallets"
            group_id = models.execute_kw(db, uid, password, 'res.groups', 'create', [{
                'name': 'Pallets',
            }])

            _logger.info('Gruppo "Pallets" creato con successo (id: %s)', group_id)

            # ottieni l'ID di tutti gli utenti del gruppo amministratori
            admin_group_id = models.execute_kw(db, uid, password, 'res.groups', 'search', [('name', '=', 'Administrators')])
            admin_users_ids = models.execute_kw(db, uid, password, 'res.users', 'search', [('groups_id', 'in', admin_group_id)])

            # associa gli utenti al gruppo "Pallets"
            models.execute_kw(db, uid, password, 'res.groups', 'write', [[group_id], {
                'users': [(6, 0, admin_users_ids)],
            }])

            _logger.info('Utenti associati al gruppo "Pallets" con successo.')                
                

        # # Cerca se esiste un gruppo con il nome "Pallets"
        # group_id = models.execute_kw(db, uid, password, 'res.groups', 'search', [[('name', '=', 'Pallets')]])
        # _logger.info(group_id)
        # # Se non esiste, crea il gruppo "Pallets" e ci associa gli utenti amministratori. 
        # if not group_id:
        #     _logger.info("Non esiste nessun gruppo Pallets \n Lo creo!")
        #     # Crea un nuovo gruppo "Pallets"
        #     vals_group = {
        #         'name': 'Pallets',
        #         'category_id': models.execute_kw(db, uid, password, 'ir.model.data', 'xmlid_to_res_id', ['base.module_category_hidden']),
        #     }
        #     new_group_id = models.execute_kw(db, uid, password, 'res.groups', 'create', [vals_group])
        #     _logger.info("Creato nuovo gruppo con il nome 'Pallets' nella tabella res.groups.")
            
        #     # Associa il gruppo appena creato ai tutti gli utenti amministratori
        #     admin_user_ids = models.execute_kw(db, uid, password, 'res.users', 'search', [[('groups_id', 'in', [models.execute_kw(db, uid, password, 'ir.model.data', 'xmlid_to_res_id', ['base.group_system'])])]])
        #     if admin_user_ids:
        #         models.execute_kw(db, uid, password, 'res.users', 'write', [admin_user_ids, {'groups_id': [(4, new_group_id)]}])
        #         _logger.info("Il gruppo 'Pallets' è stato associato agli utenti amministratori.")
        #     else:
        #         _logger.info("Non è stata trovata alcun utente amministratore.")
        # else:
        #     _logger.info("Il gruppo 'Pallets' già esiste nella tabella res.groups.")

        
        
        # Recupera il canale "Fatturazione Pallets"
        channel = self.env['mail.channel'].search([('name', '=', 'Fatturazione Pallets')], limit=1)
        if not channel:
            # Se il canale non esiste, crea il canale e aggiungi i gruppi Auto Subscribe
            _logger.info('Il canale Fatturazione Pallets non esiste. Creazione del canale e aggiunta dei gruppi Auto Subscribe.')
            pallets_group = self.env['res.groups'].search([('name', '=', 'Pallets')], limit=1)
            if not pallets_group:
                raise UserError('Il gruppo Pallets non esiste')
            auto_subscribe_groups = self.env['res.groups'].search([('id', 'in', [4, 25, 27])])
            group_ids = [(6, 0, auto_subscribe_groups.ids)]
            channel_data = {
                'name': 'Fatturazione Pallets',
                # 'message_auto_subscribe_group_ids': group_ids,
            }
            channel = self.env['mail.channel'].sudo().create(channel_data)
            _logger.info('Il canale Fatturazione Pallets è stato creato con successo.')
        else:
            # Se il canale esiste, aggiungi i gruppi Auto Subscribe
            _logger.info('Il canale Fatturazione Pallets esiste.')
        _logger.info('Inserimento degli utenti.')
        _logger.info("prima")

        self.env['mail.message.res.partner.rel'].create({
            'message_id': 1,
            'partner_id': 1,
        })
        _logger.info("dopo")
        auto_subscribe_groups = self.env['res.groups'].search([('id', 'in', [4, 25, 27])])
        group_ids = [(4, auto_subscribe_groups.ids)]
        channel.write({'message_auto_subscribe_group_ids': group_ids})
        _logger.info('I gruppi Auto Subscribe sono stati aggiunti al canale Fatturazione Pallets.')

