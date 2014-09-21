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

class oehealth_insured_group(osv.osv):
    _name = "oehealth.insured.group"
    _table= "oehealth_insured_group"
    _description = "Insured Group"

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
        'insured_id': fields.many2one('oehealth.insured', 'Titular Insured', required=True),
        #we need a related field in order to be able to sort the insured group by name
        'name': fields.related('insured_id', 'name', type='char', string='Titular Insured', 
                                readonly=True, store=True),
        'insurance_client_name': fields.related('insured_id', 'insurance_client_name', type='char', string='Insurance Client', 
                                                readonly=True, store=True),
        'insured_group_info': fields.text(string='Insured Group Info'),
        'category_ids': fields.many2many('oehealth.insured.group.category', 
                                         'oehealth_insured_group_category_rel', 
                                         'insured_group_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_insured_group_tag_rel', 
                                    'insured_group_id', 
                                    'tag_id', 
                                    'Tags'),
        'date_insured_group_inclusion' : fields.date('Insured Group Inclusion Date'),
        'insured_ids': fields.one2many('oehealth.insured.group.member',
                                       'insured_group_id',
                                       'Members'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'insured_group_id',
                                          'Annotations'),
        # 'insured_group_status': fields.selection([('U', 'Undefined'),
        #                                           ('A', 'Activated'),
        #                                           ('I', 'Inactivated'),
        #                                           ], string='Insured Group Status',
        #                                              select=True, sort=False, required=False, translate=True),
        'insured_group_status': fields.selection([('U', 'Undefined'),
                                                  ('A', 'Activated'),
                                                  ('I', 'Inactivated'),
                                                  ], string='Insured Group Status', select=True, sort=False),
        'date_insured_group_inclusion' : fields.date('Inclusion Date'),
        'date_insured_group_activation' : fields.date('Activation Date'),
        'date_insured_group_inactivation' : fields.date('Inactivation Date'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'active': fields.boolean('Active', 
                                 help="The active field allows you to hide the insured group without removing it."),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }
    
    _order='name'

    _defaults = {
        'active': 1,
        'insured_group_status': 'U',
        'state': 'new',
    }

    def oehealth_insured_group_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_insured_group_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_insured_group_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_insured_group_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_insured_group()
