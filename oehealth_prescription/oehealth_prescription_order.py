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

class oehealth_prescription_order(osv.Model):
    _name='oehealth.prescription.order'

    _columns={
        #'patient_id': fields.many2one('oehealth.patient', string='Patient', required=True),
        'pregnancy_warning': fields.boolean(string='Pregancy Warning', readonly=True),
        'notes': fields.text(string='Prescription Notes'),
        'prescription_line': fields.one2many('oehealth.prescription.line',
                                             'prescription_order_id',
                                             string='Prescription line',),
        #'pharmacy': fields.many2one('res.partner', string='Pharmacy',),
        'prescription_date': fields.datetime(string='Prescription Date'),
        #'prescription_warning_ack': fields.boolean(string='Prescription verified'),
        #'user_id': fields.many2one('res.users', string='Prescribing Doctor', required=True),
        'name': fields.char(size=256, string='Prescription ID', required=True,
                            help='Type in the ID of this prescription'),
              }
    
    _defaults={
               #'prescription_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
               #'name': lambda obj, cr, uid, context:obj.pool.get('ir.sequence').get(cr, uid,'oehealth.prescription.order'),
               }

oehealth_prescription_order()
