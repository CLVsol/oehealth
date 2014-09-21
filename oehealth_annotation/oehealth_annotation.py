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

class oehealth_annotation(osv.Model):
    _name = 'oehealth.annotation'
    _description = 'Health Annotation'

    def name_get(self, cr, uid, ids, context=None):
        """Return the annotation's display name, including their direct
           parent by default.

        :param dict context: the `annotation_display` key can be
                             used to select the short version of the
                             annotation name (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('annotation_display') == 'short':
            return super(oehealth_annotation, self).name_get(cr, uid, ids, context=context)
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
            # Be sure name_search is symetric to name_get
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
        'name' : fields.char('Reference', size=64, select=1, required=True, help='Use "/" to get an automatic new Reference.'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Reference'),
        'subject' : fields.char ('Subject',size=128, required=False),
        'from_user' : fields.many2one ('res.users', 'From'),
        'to_user' : fields.many2one ('res.users', 'To'),
        'date': fields.date("Date"),
        'body': fields.text(string='Body'),
        'category_ids': fields.many2many('oehealth.annotation.category', 
                                         'oehealth_annotation_category_rel', 
                                         'annotation_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_annotation_tag_rel', 
                                    'annotation_id', 
                                    'tag_id', 
                                    'Tags'),
        'parent_id': fields.many2one('oehealth.annotation', 'Parent Annotation', select=True, ondelete='cascade'),
        'child_ids': fields.one2many('oehealth.annotation', 'parent_id', 'Child Annotations'),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the annotation without removing it."),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
        }
    
    _constraints = [
                    (osv.osv._check_recursion, 'Error! You can not create recursive annotations.', ['parent_id'])
                    ]

    _sql_constraints = [
                        ('uniq_name', 'unique(name)', "The annotation reference must be unique!"),
                        ]

    _defaults = {
        'name': '/',
        'active': True,
        'date': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
        'from_user': lambda obj,cr,uid,context: uid, 
        'to_user': lambda obj,cr,uid,context: uid, 
        }

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'name' in vals or vals['name'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.annotation.code')
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
        return super(oehealth_annotation, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     annotations_without_code = self.search(cr, uid, [('name', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(annotations_without_code)
    #     super(oehealth_annotation, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for annotation_id in annotations_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.annotation.code')
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
    #         super(oehealth_annotation, self).write(cr, uid, annotation_id, vals, context)
    #     return True

    def copy(self, cr, uid, id, default={}, context=None):
        annotation = self.read(cr, uid, id, ['name'], context=context)
        if  annotation['name']:
            default.update({
                'name': '/',
            })
        return super(oehealth_annotation, self).copy(cr, uid, id, default, context)

oehealth_annotation()
