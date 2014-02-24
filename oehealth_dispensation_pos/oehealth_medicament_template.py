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

class oehealth_medicament_template(orm.Model):
    _inherit = 'oehealth.medicament.template'

    _columns={
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('canceled','Canceled'),
                                   ('not_authorized','Not Authorized'),
                                   ('authorized','Authorized'),
                                   ], 'Stage', readonly=True),
        'state_msg': fields.char(size=256,
                                 string='Stage Message', 
                                 help='Stage Message'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'medicament_template_id',
                                          'Annotations'),
        }
    
    _defaults = {
         'state': 'new',
    }
    
    def oehealth_medicament_tmpl_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         #self.write(cr, uid, ids, {'state_msg': ''})
         return True

    def oehealth_medicament_tmpl_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         self.write(cr, uid, ids, {'state_msg': ''})
         return True

    def oehealth_medicament_tmpl_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         self.write(cr, uid, ids, {'state_msg': ''})
         return True

    def oehealth_medicament_tmpl_canceled(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'canceled'})
         self.write(cr, uid, ids, {'state_msg': ''})
         return True

    def oehealth_medicament_tmpl_not_authorized(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'not_authorized'})
         self.write(cr, uid, ids, {'state_msg': ''})
         return True

    def oehealth_medicament_tmpl_authorized(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'authorized'})
         self.write(cr, uid, ids, {'state_msg': 'Manual Authorization'})
         return True

oehealth_medicament_template()
