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
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

class oehealth_patient_mng(osv.Model):
    _name = 'oehealth.patient_mng'
    _description = "Health Insured Management"

    def _compute_age(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        now = datetime.now()
        for r in self.browse(cr, uid, ids, context=context):
            if r.birthday:
                dob = datetime.strptime(r.birthday,'%Y-%m-%d')
                delta=relativedelta (now, dob)
                result[r.id] = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            else:
                result[r.id] = "No Date of Birth!"
        return result

    _columns = {
        'category_ids': fields.many2many('oehealth.patient_mng.category', 
                                         'oehealth_patient_mng_category_rel', 
                                         'patient_mng_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_patient_mng_tag_rel', 
                                    'insured_id', 
                                    'tag_id', 
                                    'Tags'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('processing','Processing'),
                                   ('okay','Okay')], 'Stage', readonly=True),



        'name': fields.char('Name', size=128, required=True, select=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Insured is referred'),
        'patient_category': fields.char('Patient Category', size=64),
        'birthday': fields.date("Date of Birth"),
        'age' : fields.function(_compute_age, method=True, type='char', size=32, string='Age',),
        'mother_name': fields.char('Mother Name', size=128),
        'father_name': fields.char('Father Name', size=128),
        'responsible_name': fields.char('Responsible Name', size=128),
        'identification_id': fields.char('Person ID', size=10),
        'otherid': fields.char('Other ID', size=64),
        'gender': fields.selection([('M', 'Male'),('F', 'Female')], 'Gender'),
        'marital': fields.selection([('single', 'Single'), 
                                     ('married', 'Married'), 
                                     ('widower', 'Widower'), 
                                     ('divorced', 'Divorced'),
                                     ], 'Marital Status'),
        'street': fields.char('Street', size=128),
        'street2': fields.char('Street2', size=128),
#        'district': fields.char('Bairro', size=32),
        'number': fields.char('Number', size=10),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City', size=128),
        'country': fields.char('Country Name', size=64, help='The full name of the country.', required=False, translate=True),
        'country_state': fields.char('State Name', size=64, required=False, 
                                     help='Administrative divisions of a country. E.g. Fed. State, Departement, Canton'),
        'email': fields.char('Email', size=240),
        'phone': fields.char('Phone', size=64),
        'fax': fields.char('Fax', size=64),
        'mobile': fields.char('Mobile', size=64),



        'date_patient_inclusion' : fields.date('Patient Inclusion Date'),
        'date_patient_activation' : fields.date('Patient Activation Date'),
        'date_patient_inactivation' : fields.date('Patient Inactivation Date'),
        # 'patient_status': fields.selection([('U', 'Undefined'),
        #                                     ('A', 'Activated'),
        #                                     ('I', 'Inactivated'),
        #                                     ], string='Patient Status',
        #                                        select=True, sort=False, required=False, translate=True),
        'patient_status': fields.selection([('U', 'Undefined'),
                                            ('A', 'Activated'),
                                            ('I', 'Inactivated'),
                                            ], string='Patient Status', select=True, sort=False),



        'country_id': fields.many2one('res.country', 'Nationality'),
        'state_id': fields.many2one("res.country.state", 'State'),
        #'l10n_br_city_id': fields.many2one('l10n_br_base.city', 'City',
        #                                   domain="[('state_id','=',state_id)]"),
        'patient': fields.many2one('oehealth.patient', 'Related Patient', required=False,
                                   help='Patient-related data of the patient'),
        'person': fields.many2one('oehealth.person', 'Related Person', required=False,
                                   help='Person-related data of the patient'),
        'person_mother': fields.many2one('oehealth.person', 'Related Mother', required=False,
                                   help='Mother-related data of the mother'),
        'person_father': fields.many2one('oehealth.person', 'Related Father', required=False,
                                   help='Father-related data of the father'),
        'person_responsible': fields.many2one('oehealth.person', 'Related Responsible', required=False,
                                   help='Responsible-related data of the responsible'),
        'active': fields.boolean('Active', help="The active field allows you to hide the insured without removing it."),
    }

    _order='name'

    _defaults = {
        'active': 1,
        'state': 'new',
    }
    
    def oehealth_patient_mng_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_patient_mng_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_patient_mng_processing(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'processing'})
         return True

    def oehealth_patient_mng_done(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_patient_mng()
