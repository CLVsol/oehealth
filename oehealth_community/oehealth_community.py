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

class oehealth_community(osv.osv):
    _name = "oehealth.community"
    _table= "oehealth_community"
    _description = "Community"
    _inherits={
               'res.partner': 'partner',
               }

    def name_get(self, cr, uid, ids, context=None):
        """Return the community' display name, including their direct
           parent by default.

        :param dict context: the ``oehealth_community_display`` key can be
                             used to select the short version of the
                             speciality name (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('oehealth_community_display') == 'short':
            return super(oehealth_community, self).name_get(cr, uid, ids, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

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
                                    ondelete='cascade', help='Partner-related data of the Community'),
        #we need a related field in order to be able to sort the person by name
        'name_related': fields.related('partner', 'name', type='char', string='Related Partner', 
                                       readonly=True, store=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Community is referred'),
        'community_code': fields.char(size=64, string='Community Code', required=False),
        'parent_id': fields.many2one('oehealth.community', 'Parent Community', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name', store=True),
        'child_ids': fields.one2many('oehealth.community', 'parent_id', 'Child Communities'),
        #'parent_left': fields.integer('Left parent', select=True),
        #'parent_right': fields.integer('Right parent', select=True),
        'community_info': fields.text(string='Community Info'),
        'community_info2': fields.text(string='Community Info-2'),
        'category_ids': fields.many2many('oehealth.community.category', 
                                         'oehealth_community_category_rel', 
                                         'community_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_community_tag_rel', 
                                    'community_id', 
                                    'tag_id', 
                                    'Tags'),
        'date_community_inclusion' : fields.date('Community Inclusion Date'),
        'person_ids': fields.one2many('oehealth.community.person.member',
                                      'community_id',
                                      'Person Members'),
        'family_ids': fields.one2many('oehealth.community.family.member',
                                      'community_id',
                                      'Family Members'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'community_id',
                                          'Annotations'),
        # 'community_status': fields.selection([('U', 'Undefined'),
        #                                       ('A', 'Activated'),
        #                                       ('I', 'Inactivated'),
        #                                       ], string='Community Status',
        #                                          select=True, sort=False, required=False, translate=True),
        'community_status': fields.selection([('U', 'Undefined'),
                                              ('A', 'Activated'),
                                              ('I', 'Inactivated'),
                                              ], string='Community Status', select=True, sort=False),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order = 'complete_name'

    _constraints = [
        (osv.osv._check_recursion, 'Error! You can not create recursive communities.', ['parent_id'])
        ]

    _defaults = {
        'health_partner_code': '/',
        'community_code': '/',
        'active': 1,
        'is_health_partner': True,
        'is_community': True,
        'customer': False,
        'supplier': False,
        'is_company': True,
        'state': 'new',
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'community_code' in vals or vals['community_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.community.code')
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
                vals['community_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['community_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['community_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['community_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['community_code'] = code_str[14 - code_len:21]
        return super(oehealth_community, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     communities_without_code = self.search(cr, uid, [('community_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(communitys_without_code)
    #     super(oehealth_community, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in communities_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.community.code')
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
    #             vals['community_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['community_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['community_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['community_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['community_code'] = code_str[14 - code_len:21]
    #         super(oehealth_community, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_community_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_community_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_community_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_community_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_community()
