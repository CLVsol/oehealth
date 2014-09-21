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


class oehealth_medicament_template(osv.Model):
    _name = 'oehealth.medicament.template'
    _description = "Medicament Template"

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
        'name': fields.char(string='Medicament Template Code', size=64, required=True,  
                            help='Medicament Template Code'),
        'medicament': fields.many2one('oehealth.medicament',
                                      string='Medicament',
                                      required=True, 
                                      help='Prescribed Medicament'),
        'form': fields.many2one('oehealth.drug.form', string='Form', 
                                 help='Drug form, such as tablet or gel'),
        'route': fields.many2one('oehealth.drug.route',
                                 string='Administration Route', 
                                 help='Drug administration route code.'),
        'dose': fields.float(string='Dose', 
                             help='Amount of medicament (eg, 250 mg) per dose'),
        'dose_unit': fields.many2one('product.uom',
                                     string='dose unit', 
                                     help='Unit of measure for the medicament to be taken'),
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
                                            ], string='frequency unit',select=True, sort=False),
        'duration': fields.integer(string='Treatment duration',
                                   help='Period that the patient must take the medicament. in minutes, '\
                                        'hours, days, months, years or indefinately'),
        'duration_period': fields.selection([('minutes', 'minutes'),
                                             ('hours', 'hours'),
                                             ('days', 'days'),
                                             ('weeks', 'weeks'),
                                             ('months', 'months'),
                                             ('years', 'years'),
                                             ('indefinite', 'indefinite'),
                                             ('continuous use', 'continuous use'),
                                             ], string='Treatment period',
                                            help='Period that the patient must take the medicament in minutes,'\
                                                 ' hours, days, months, years or indefinately'),
        'admin_times': fields.char(size=256, string='Administration hours', 
                                   help='Suggested administration hours. For example, at 08:00, 13:00'\
                                        ' and 18:00 can be encoded like 08 13 18'),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
        }

    _order='name'

    _sql_constraints = [('medicamente_template_code_uniq', 'unique(name)', u'Duplicated Medicamente Template Code!')]

    _defaults = {
        'name': '/',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'name' in vals or vals['name'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament_tmpl.code')
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
        return super(oehealth_medicament_template, self).create(cr, uid, vals, context)

oehealth_medicament_template()
