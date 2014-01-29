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


class oehealth_medication_template(osv.Model):
    _name = 'oehealth.medication.template'

    _columns = {
        'name': fields.char(size=256, string='Name'),
        'medication': fields.many2one('oehealth.medicament',
                                      string='Medication',
                                      required=True, 
                                      help='Prescribed Medication'),
        'form': fields.many2one('oehealth.drug.form', string='Form', 
                                 help='Drug form, such as tablet or gel'),
        'route': fields.many2one('oehealth.drug.route',
                                 string='Administration Route', 
                                 help='Drug administration route code.'),
        'dose': fields.float(string='Dose', 
                             help='Amount of medication (eg, 250 mg) per dose'),
        'dose_unit': fields.many2one('product.uom',
                                     string='dose unit', 
                                     help='Unit of measure for the medication to be taken'),
        'quantity': fields.integer(string='Medicament Quantity',
                              help='Quantity of units (eg, 2 capsules) of the medicament'),
        'frequency': fields.integer(string='Frequency', 
                                    help='Time in between doses the patient must wait (ie, for 1 pill'\
                                    ' each 8 hours, put here 8 and select \"hours\" in the unit field'),
        'frequency_unit': fields.selection([('seconds', 'seconds'),
                                            ('minutes', 'minutes'),
                                            ('hours', 'hours'),
                                            ('days', 'days'),
                                            ('weeks', 'weeks'),
                                            ('wr', 'when required'),
                                            ], string='unit',select=True, sort=False),
        'duration': fields.integer(string='Treatment duration',
                                   help='Period that the patient must take the medication. in minutes, '\
                                   'hours, days, months, years or indefinately'),
        'duration_period': fields.selection([('minutes', 'minutes'),
                                             ('hours', 'hours'),
                                             ('days', 'days'),
                                             ('months', 'months'),
                                             ('years', 'years'),
                                             ('indefinite', 'indefinite'),
                                             ('continuous use', 'continuous use'),
                                             ], string='Treatment period',
                                            help='Period that the patient must take the medication in minutes,'\
                                                 ' hours, days, months, years or indefinately'),
        'admin_times': fields.char(size=256, string='Administration hours', 
                                   help='Suggested administration hours. For example, at 08:00, 13:00'\
                                        ' and 18:00 can be encoded like 08 13 18'),
        }

oehealth_medication_template()
