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

class oehealth_family(osv.osv):
    _name = "oehealth.family"
    _table= "oehealth_family"
    _description = "Family"
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
                                   ondelete='cascade', help='Partner-related data of the Person'),
        #we need a related field in order to be able to sort the person by name
        'name_related': fields.related('partner', 'name', type='char', string='Related Partner', 
                                       readonly=True, store=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Person is referred'),
        'family_code': fields.char(size=64, string='Family Code', required=False),
        'family_info': fields.text(string='Family Info'),
        'family_info2': fields.text(string='Family Info-2'),
        'category_ids': fields.many2many('oehealth.family.category', 
                                         'oehealth_family_category_rel', 
                                         'family_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_family_tag_rel', 
                                    'family_id', 
                                    'tag_id', 
                                    'Tags'),
        'date_family_inclusion' : fields.date('Family Inclusion Date'),
        'person_ids': fields.one2many('oehealth.family.member',
                                      'family_id',
                                      'Members'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'family_id',
                                          'Annotations'),
        # 'family_status': fields.selection([('U', 'Undefined'),
        #                                    ('A', 'Activated'),
        #                                    ('I', 'Inactivated'),
        #                                    ], string='Family Status',
        #                                       select=True, sort=False, required=False, translate=True),
        'family_status': fields.selection([('U', 'Undefined'),
                                           ('A', 'Activated'),
                                           ('I', 'Inactivated'),
                                           ], string='Family Status', select=True, sort=False),
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

    _defaults = {
        'health_partner_code': '/',
        'family_code': '/',
        'active': 1,
        'is_health_partner': True,
        'is_family': True,
        'customer': False,
        'supplier': False,
        'is_company': True,
        'family_status': 'U',
        'state': 'new',
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'family_code' in vals or vals['family_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.family.code')
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
                vals['family_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['family_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['family_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['family_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['family_code'] = code_str[14 - code_len:21]
        return super(oehealth_family, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     families_without_code = self.search(cr, uid, [('family_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(families_without_code)
    #     super(oehealth_family, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in families_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.family.code')
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
    #             vals['family_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['family_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['family_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['family_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['family_code'] = code_str[14 - code_len:21]
    #         super(oehealth_family, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_family_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_family_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_family_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_family_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_family()
