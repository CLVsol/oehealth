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
from datetime import datetime
from dateutil.relativedelta import relativedelta

class oehealth_person(osv.Model):
    _name = 'oehealth.person'
    _description = "Health Person"
    _inherits={
               'res.partner': 'partner',
               }

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
                                   ondelete='cascade', help='Partner-related data of the person'),
        #we need a related field in order to be able to sort the person by name
        'name_related': fields.related('partner', 'name', type='char', string='Related Partner', 
                                       readonly=True, store=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Person is referred'),
        'person_code': fields.char(size=64, string='Person Code', required=False),
        'person_category_ids': fields.many2many('oehealth.person.category', 
                                                'oehealth_person_category_rel', 
                                                'person_id', 
                                                'category_id', 
                                                'Categories'),
        'person_tag_ids': fields.many2many('oehealth.tag', 
                                           'oehealth_person_tag_rel', 
                                           'person_id', 
                                           'tag_id', 
                                           'Tags'),
        'person_info': fields.text(string='Person Info'),
        'person_info2': fields.text(string='Person Info-2'),
        'date_person_inclusion' : fields.date('Inclusion Date'),
        'date_person_activation' : fields.date('Activation Date'),
        'date_person_inactivation' : fields.date('Inactivation Date'),
        'country_id': fields.many2one('res.country', 'Nationality'),
        'birthday': fields.date("Date of Birth"),
        'age' : fields.function(_compute_age, method=True, type='char', size=32, string='Age',),
        'spouse_id': fields.many2one('oehealth.person', 'Spouse'),
        'father_id': fields.many2one('oehealth.person', 'Father'),
        'mother_id': fields.many2one('oehealth.person', 'Mother'),
        'responsible_id': fields.many2one('oehealth.person', 'Responsible'),
        'identification_id': fields.char('Person ID', size=10),
        'otherid': fields.char('Other ID', size=64),
        'gender': fields.selection([('M', 'Male'),('F', 'Female')], 'Gender'),
        'marital': fields.selection([('single', 'Single'), 
                                     ('married', 'Married'), 
                                     ('widower', 'Widower'), 
                                     ('divorced', 'Divorced'),
                                     ], 'Marital Status'),
        'events_ids': fields.one2many('oehealth.event.participant',
                                      'person_id',
                                      'Events'),
        'person_annotation_ids': fields.one2many('oehealth.annotation',
                                                 'person_id',
                                                 'Person Annotations'),
        # 'person_status': fields.selection([('U', 'Undefined'),
        #                                    ('A', 'Activated'),
        #                                    ('I', 'Inactivated'),
        #                                    ], string='Person Status',
        #                                       select=True, sort=False, required=False, translate=True),
        'person_status': fields.selection([('U', 'Undefined'),
                                           ('A', 'Activated'),
                                           ('I', 'Inactivated'),
                                           ], string='Person Status', select=True, sort=False),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order='name_related'

    _sql_constraints = [('person_code_uniq', 'unique(person_code)', u'Duplicated Person Code!')]

    _defaults = {
        'health_partner_code': '/',
        'person_code': '/',
        'active': 1,
        'customer': False,
        'supplier': False,
        'is_company': False,
        'is_health_partner': True,
        'is_person': True,
        'person_status': 'U',
        'state': 'new',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'person_code' in vals or vals['person_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.person.code')
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
                vals['person_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['person_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['person_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['person_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['person_code'] = code_str[14 - code_len:21]
        return super(oehealth_person, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     persons_without_code = self.search(cr, uid, [('person_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(persons_without_code)
    #     super(oehealth_person, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in persons_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.person.code')
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
    #             vals['person_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['person_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['person_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['person_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['person_code'] = code_str[14 - code_len:21]
    #         super(oehealth_person, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_person_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_person_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_person_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_person_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_person()
