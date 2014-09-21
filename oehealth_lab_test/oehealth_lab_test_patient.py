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
import time

class oehealth_lab_test_patient(osv.osv):
    _name = 'oehealth.lab_test.patient'
    
    #def _get_default_dr(self, cr, uid, context={}):
    #    partner_id = self.pool.get('res.partner').search(cr,uid,[('user_id','=',uid)])
    #    if partner_id:
    #        dr_id = self.pool.get('hr.employee').search(cr,uid,[('name','=',partner_id[0])])
    #        if dr_id:
    #            return dr_id[0]
            #else:
            #    raise osv.except_osv(_('Error !'),
            #            _('There is no physician defined ' \
            #                    'for current user.'))
     #   else:
     #       return False
        
    _columns = {
        'name' : fields.many2one('oehealth.lab_test.type','Lab Test Type'),
        'date' : fields.datetime('Date'),
        'state' : fields.selection([('draft','Draft'),
                                    ('tested','Tested'),
                                    ('cancel','Cancel')],
                                   'State',readonly=True),
        'patient_id' : fields.many2one('oehealth.patient','Patient'),
        'professional_id' : fields.many2one('oehealth.professional','Health Professional', 
                                         help="Health Professional who Request the lab test."), 
        'invoice_status' : fields.selection([('invoiced','Invoiced'),
                                             ('tobe','To be Invoiced'),
                                             ('no','No Invoice')],
                                            'Invoice Status'),
        'lab_test_id': fields.many2one('oehealth.lab_test','name','Patient Lab Test'),
        }
    
    _defaults={
       'date' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
       'state' : lambda *a : 'draft',
       #'doctor_id' : _get_default_dr,        
       'invoice_status': lambda *a: 'tobe',
       }

oehealth_lab_test_patient()
