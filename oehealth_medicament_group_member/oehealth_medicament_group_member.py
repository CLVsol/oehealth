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

class oehealth_medicament_group_member(osv.Model):
    _name = 'oehealth.medicament.group.member'

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
        'group_id': fields.many2one('oehealth.medicament.group', string='Medicament Group',
                                    help='Medicament Group', required=True),
        'medicament_id': fields.many2one('oehealth.medicament', string='Medicament',
                                         help='Medicament Name', required=True),
        'category': fields.many2one('oehealth.medicament.group.member.category', 'Category', required=False),
        'info': fields.text(string='Info'),
        'level': fields.integer(string='Level'),
        'order': fields.integer(string='Order'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_medicament_group_member_tag_rel', 
                                    'medicament_group_member_id', 
                                    'tag_id', 
                                    'Medicament Group Member Tags'),
        'group_member_annotation_ids': fields.one2many('oehealth.annotation',
                                                       'medicament_group_member_id',
                                                       'Group Member Annotations'),
        # 'group_status': fields.selection([('U', 'Undefined'),
        #                                   ('A', 'Activated'),
        #                                   ('I', 'Inactivated'),
        #                                   ], string='Medicament Group Status',
        #                                      select=True, sort=False, required=False, translate=True),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }
    
    _order='level'
    
    _defaults = {
        'level': 9,
        'order': 90,
        'state': 'new',
        }

    def oehealth_medicament_group_member_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_medicament_group_member_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_medicament_group_member_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_medicament_group_member_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_medicament_group_member()
