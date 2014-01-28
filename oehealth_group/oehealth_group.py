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
from openerp.tools.translate import _
import datetime

class oehealth_group(osv.Model):
    _name = 'oehealth.group'
    _description = 'Health Group'

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
        'name' : fields.char('Reference', size=64, select=1, required=True, help='Use "/" to get an automatic new Reference.'),
        'subject' : fields.char ('Subject',size=128, required=False),
        'responsible' : fields.many2one ('res.users', 'Responsible'),
        'date_group_inclusion' : fields.date('Group Inclusion Date'),
        'group_info': fields.text(string='Group Info'),
        'group_category_ids': fields.many2many('oehealth.group.category', 
                                               'oehealth_group_category_rel', 
                                               'group_id', 
                                               'category_id', 
                                               'Categories'),
        'group_tag_ids': fields.many2many('oehealth.tag', 
                                          'oehealth_group_tag_rel', 
                                          'group_id', 
                                          'tag_id', 
                                          'Tags'),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the group without removing it."),
        'group_annotation_ids': fields.one2many('oehealth.annotation',
                                                'group_id',
                                                'Annotations'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'participant_ids': fields.one2many('oehealth.group.participant',
                                           'group_id',
                                           'Participants'),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
        }

    _sql_constraints = [
                        ('uniq_name', 'unique(name)', "The group name must be unique!"),
                        ]

    _defaults = {
        'name': '/',
        'active': True,
        'date_group_inclusion': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
        'responsible': lambda obj,cr,uid,context: uid, 
        'state': 'new',
        }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'name' in vals or vals['name'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.group.code')
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
                vals['name'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['name'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['name'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['name'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['name'] = code_str[14 - code_len:21]
        return super(oehealth_group, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     groups_without_code = self.search(cr, uid, [('name', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(groups_without_code)
    #     super(oehealth_group, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in groups_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.group.code')
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
    #             vals['name'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['name'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['name'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['name'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['name'] = code_str[14 - code_len:21]
    #         super(oehealth_group, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_group_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_group_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_group_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_group_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_group()
