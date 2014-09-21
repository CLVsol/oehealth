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

from osv import osv
from osv import fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class oehealth_insurance_client(osv.Model):
    _name = 'oehealth.insurance_client'
    _description = "Insurance Client"
    _inherits={
               'res.partner': 'partner',
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

    _columns = {
        'partner': fields.many2one('res.partner', 'Related Partner', required=True,
                                   ondelete='cascade', help='Partner-related data of the insurance_client'),
        #we need a related field in order to be able to sort the insurance_client by name
        'name_related': fields.related('partner', 'name', type='char', string='Related Partner', 
                                       readonly=True, store=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Insurance Client is referred'),
        'insurance_client_code': fields.char(size=64, string='Insurance Client Code', required=False),
        'category_ids': fields.many2many('oehealth.insurance_client.category', 
                                         'oehealth_insurance_client_category_rel', 
                                         'insurance_client_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_insurance_client_tag_rel', 
                                    'insurance_client_id', 
                                    'tag_id', 
                                    'Tags'),
        'insurance_client_info': fields.text(string='Info'),
        'insurance_client_info2': fields.text(string='Info-2'),
        'date_insurance_client_inclusion' : fields.date('Inclusion Date'),
        'date_insurance_client_activation' : fields.date('Activation Date'),
        'date_insurance_client_inactivation' : fields.date('Inactivation Date'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'insurance_client_id',
                                          'Annotations'),
        # 'insurance_client_status': fields.selection([
        #                                      ('U', 'Undefined'),
        #                                      ('A', 'Activated'),
        #                                      ('I', 'Inactivated'),
        #                                      ], string='Status',
        #                                         select=True, sort=False, required=False, translate=True),
        'insurance_client_status': fields.selection([('U', 'Undefined'),
                                                     ('A', 'Activated'),
                                                     ('I', 'Inactivated'),
                                                     ], string='Insurance Client Status', select=True, sort=False),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order='name_related'

    _sql_constraints = [('insurance_client_code_uniq', 'unique(insurance_client_code)', u'Duplicated Insurance Client Code!')]

    _defaults = {
        'health_partner_code': '/',
        'insurance_client_code': '/',
        'active': 1,
        'customer': True,
        'supplier': False,
        'is_company': True,
        'is_health_partner': True,
        'is_insurance_client': True,
        'insurance_client_status': 'U',
        'state': 'new',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'insurance_client_code' in vals or vals['insurance_client_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.insurance_client.code')
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
                vals['insurance_client_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['insurance_client_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['insurance_client_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['insurance_client_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['insurance_client_code'] = code_str[14 - code_len:21]
        return super(oehealth_insurance_client, self).create(cr, uid, vals, context)

    def oehealth_insurance_client_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_insurance_client_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_insurance_client_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_insurance_client_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_insurance_client()
