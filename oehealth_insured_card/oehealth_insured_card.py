# -*- encoding: utf-8 -*-
################################################################################
#                                                                              #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                  #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Affero General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU Affero General Public License for more details.                          #
#                                                                              #
# You should have received a copy of the GNU Affero General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
################################################################################

from osv import fields, osv
from datetime import datetime
from dateutil.relativedelta import relativedelta

class oehealth_insured_card(osv.osv):
    _name = "oehealth.insured.card"
    _table= "oehealth_insured_card"
    _description = "Health Insured Card"
    _inherits={
               'oehealth.insured': 'insured',
               }

    def _compute_create_uid(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            create_uid = perms[0].get('create_uid', 'n/a')
            result[r.id] = create_uid
        return result

    def _compute_create_date(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            create_date = perms[0].get('create_date', 'n/a')
            result[r.id] = create_date
        return result

    def _compute_write_uid(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            write_uid = perms[0].get('write_uid', 'n/a')
            result[r.id] = write_uid
        return result

    def _compute_write_date(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            perms = self.perm_read(cr, uid, ids)
            write_date = perms[0].get('write_date', 'n/a')
            result[r.id] = write_date
        return result

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name_card_number'], context=context)
        res = []
        for record in reads:
            name = record['name_card_number']
            res.append((record['id'], name))
        return res
    
    def name_card_number_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        #reads = self.read(cr, uid, ids, ['name', 'card_number'], context=context)
        reads = self.read(cr, uid, ids, ['printed_name', 'card_number'], context=context)
        res = []
        for record in reads:
            #name = record['name']
            if record['printed_name']:
            	name = record['printed_name']
            else:
            	name = ''
            if record['card_number']:
                name = name + ' (' + record['card_number'] + ')'
            res.append((record['id'], name))
        return res

    def _name_card_number_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_card_number_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'printed_name' : fields.char('Name', size=35, help='Name printed on the card.'),
        'card_number': fields.char('Card Number', required=False, size=64, translate=False),
        'insured_card_code': fields.char(size=64, string='Card Code', required=False),
        'name_card_number': fields.function(_name_card_number_get_fnc, type="char", string='Name (Card Number)'),
        'insured': fields.many2one('oehealth.insured', 'Insured', required=False,
                                   ondelete='cascade', help='Insured-related data of the card'),
        'insured_card_info': fields.text(string='Info'),
        'insured_card_category_ids': fields.many2many('oehealth.insured.card.category', 
                                                      'oehealth_insured_card_category_rel', 
                                                      'insured_card_id', 
                                                      'category_id', 
                                                      'Categories'),
        'insured_card_tag_ids': fields.many2many('oehealth.tag', 
                                                 'oehealth_insured_card_tag_rel', 
                                                 'insured_card_id', 
                                                 'tag_id', 
                                                 'Tags'),
        'date_insured_card_inclusion' : fields.date('Inclusion Date'),
        'date_insured_card_activation' : fields.date('Activation Date'),
        'date_insured_card_inactivation' : fields.date('Inactivation Date'),
        'date_insured_card_suspension' : fields.date('Suspension Date'),
        'date_insured_card_expiration' : fields.date('Expiration Date'),
        # 'insured_card_status': fields.selection([('U', 'Undefined'),
        #                                          ('A', 'Activated'),
        #                                          ('I', 'Inactivated'),
        #                                          ('S', 'Suspended'),
        #                                          ('E', 'Expired'),
        #                                          ], string='Insured Card Status',
        #                                             select=True, sort=False, required=False, translate=True),
        'insured_card_status': fields.selection([('U', 'Undefined'),
                                                 ('A', 'Activated'),
                                                 ('I', 'Inactivated'),
                                                 ('S', 'Suspended'),
                                                 ('E', 'Expired'),
                                                 ], string='Insured Card Status', select=True, sort=False),
        'insured_card_annotation_ids': fields.one2many('oehealth.annotation',
                                                       'insured_card_id',
                                                       'Annotations'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order='card_number'

    _sql_constraints = [('card_number_uniq', 'unique(card_number)', u'Duplicated Insured Card Number!')]

    _defaults = {
        'health_partner_code': '/',
        'insured_code': '/',
        'insured_card_code': '/',
        'active': 1,
        'customer': False,
        'supplier': False,
        'is_company': False,
        'is_health_partner': True,
        'is_insured': True,
        'is_insured_card': True,
        'state': 'new',
        'insured_card_status': 'U',
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'insured_card_code' in vals or vals['insured_card_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.insured_card.code')
            code = map(int, str(val))
            code_len = len(code)
            while len(code) < 14:
                code.insert(0, 0)
            while len(code) < 16:
                n = sum([(len(code) + 1 - i) * v for i, v in enumerate(code)]) % 11
                if n > 1:
                    f = 11 - n
                else:
                    f = 0
                code.append(f)
            code_str = "%s.%s.%s.%s.%s-%s" % (str(code[0]) + str(code[1]),
                                              str(code[2]) + str(code[3]) + str(code[4]),
                                              str(code[5]) + str(code[6]) + str(code[7]),
                                              str(code[8]) + str(code[9]) + str(code[10]),
                                              str(code[11]) + str(code[12]) + str(code[13]),
                                              str(code[14]) + str(code[15]))
            if code_len <= 3:
                vals['insured_card_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['insured_card_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['insured_card_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['insured_card_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['insured_card_code'] = code_str[14 - code_len:21]
        return super(oehealth_insured_card, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     insured_cards_without_code = self.search(cr, uid, [('insured_card_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(insured_cards_without_code)
    #     super(oehealth_insured_card, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in insured_cards_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.insured_card.code')
    #         code = map(int, str(val))
    #         code_len = len(code)
    #         while len(code) < 14:
    #             code.insert(0, 0)
    #         while len(code) < 16:
    #             n = sum([(len(code) + 1 - i) * v for i, v in enumerate(code)]) % 11
    #             if n > 1:
    #                 f = 11 - n
    #             else:
    #                 f = 0
    #             code.append(f)
    #         code_str = "%s.%s.%s.%s.%s-%s" % (str(code[0]) + str(code[1]),
    #                                           str(code[2]) + str(code[3]) + str(code[4]),
    #                                           str(code[5]) + str(code[6]) + str(code[7]),
    #                                           str(code[8]) + str(code[9]) + str(code[10]),
    #                                           str(code[11]) + str(code[12]) + str(code[13]),
    #                                           str(code[14]) + str(code[15]))
    #         if code_len <= 3:
    #             vals['insured_card_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['insured_card_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['insured_card_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['insured_card_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['insured_card_code'] = code_str[14 - code_len:21]
    #         super(oehealth_insured_card, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_insured_card_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_insured_card_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_insured_card_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_insured_card_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True
