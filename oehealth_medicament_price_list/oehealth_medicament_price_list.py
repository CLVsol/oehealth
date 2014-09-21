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

class oehealth_medicament_price_list(osv.osv):
    _description = 'Health Medicament Prece Lists'
    _name = 'oehealth.medicament.price_list'
    
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

    _columns = {
        'name': fields.char('Medicament Price List Name', required=True, size=64, translate=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Medicament Price List is referred'),
        'price_list_code': fields.char(size=64, string='Medicament Price List Code', required=False),
        'medicament_price_list_item_ids': fields.one2many('oehealth.medicament.price_list.item',
                                                          'price_list_id',
                                                          'Medicament Price List Item'),
        'active': fields.boolean('Active', help="The active field allows you to hide the medicament price list without removing it."),
        'price_list_info': fields.text(string='Info'),
        'date_price_list_inclusion' : fields.date('Price List Inclusion Date'),
        'date_price_list_activation' : fields.date('Price List Activation Date'),
        'date_price_list_inactivation' : fields.date('Price List Inactivation Date'),
        'price_list_category': fields.many2one('oehealth.medicament.price_list.category',
                                               'Category',select=True),
        'price_list_tag_ids': fields.many2many('oehealth.tag', 
                                               'oehealth_medicament_price_list_tag_rel', 
                                               'price_list_id', 
                                               'tag_id', 
                                               'Tags'),
        # 'price_list_status': fields.selection([('U', 'Undefined'),
        #                                        ('A', 'Activated'),
        #                                        ('I', 'Inactivated'),
        #                                        ], string='Medicament Price List Status',
        #                                           select=True, sort=False, required=False, translate=True),
        'price_list_status': fields.selection([('U', 'Undefined'),
                                               ('A', 'Activated'),
                                               ('I', 'Inactivated'),
                                               ], string='Medicament Price List Status', select=True, sort=False),
        'price_list_annotation_ids': fields.one2many('oehealth.annotation',
                                                     'medicament_price_list_id',
                                                     'Items'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _sql_constraints = [('price_list_code_uniq', 'unique(price_list_code)', u'Duplicated Price List Code!')]
    
    _defaults = {
        'price_list_code': '/',
        'active': 1,
        'price_list_status': 'U',
        'state': 'new',
    }
    
    _order = 'name'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'price_list_code' in vals or vals['price_list_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament_prlist.code')
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
                vals['price_list_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['price_list_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['price_list_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['price_list_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['price_list_code'] = code_str[14 - code_len:21]
        return super(oehealth_medicament_price_list, self).create(cr, uid, vals, context)

    def oehealth_medicament_price_list_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_medicament_price_list_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_medicament_price_list_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_medicament_price_list_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_medicament_price_list()
