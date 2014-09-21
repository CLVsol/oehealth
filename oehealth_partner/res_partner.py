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

from openerp.osv import orm, fields
import re


class res_partner(orm.Model):
    _inherit = 'res.partner'

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
        'is_health_partner' : fields.boolean('Is a Health Partner', help="Check if the partner is a health partner."),
        'health_partner_code': fields.char(size=64, string='Health Partner Code', required=False),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'partner_id',
                                          'Annotations'),
        'health_tag_ids': fields.many2many('oehealth.tag', 
                                           'oehealth_partner_tag_rel', 
                                           'partner_id', 
                                           'tag_id', 
                                           'Health Tags'),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _sql_constraints = [('health_partner_code_uniq', 'unique(health_partner_code)', u'Duplicated Health Partner Code!')]

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}

        if (not 'is_health_partner' in vals or vals['is_health_partner'] == False):
            return super(res_partner, self).create(cr, uid, vals, context)
                
        if not 'health_partner_code' in vals or vals['health_partner_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.partner.code')
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
                vals['health_partner_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['health_partner_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['health_partner_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['health_partner_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['health_partner_code'] = code_str[14 - code_len:21]
        return super(res_partner, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        
        if context is None:
            context = {}

        partners_without_code = self.search(cr, uid, [('health_partner_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
        direct_write_ids = set(ids) - set(partners_without_code)
        super(res_partner, self).write(cr, uid, list(direct_write_ids), vals, context)
        
        for partner_id in partners_without_code:
            if (not 'is_health_partner' in vals or vals['is_health_partner'] == False):
                super(res_partner, self).write(cr, uid, partner_id, vals, context)
            elif not 'health_partner_code' in vals or vals['health_partner_code'] == '/':
                val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.partner.code')
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
                    vals['health_partner_code'] = code_str[18 - code_len:21]
                elif code_len > 3 and code_len <= 6:
                    vals['health_partner_code'] = code_str[17 - code_len:21]
                elif code_len > 6 and code_len <= 9:
                    vals['health_partner_code'] = code_str[16 - code_len:21]
                elif code_len > 9 and code_len <= 12:
                    vals['health_partner_code'] = code_str[15 - code_len:21]
                elif code_len > 12 and code_len <= 14:
                    vals['health_partner_code'] = code_str[14 - code_len:21]
                vals['is_health_partner'] = True
                super(res_partner, self).write(cr, uid, partner_id, vals, context)
        return True

res_partner()
