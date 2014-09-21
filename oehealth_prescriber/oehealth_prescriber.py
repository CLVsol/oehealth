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

class oehealth_prescriber(osv.Model):
    _name = 'oehealth.prescriber'
    _description = "Health Prescriber"
    _inherits={
               'res.partner': 'partner',
               }

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

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name_prescriber_code'], context=context)
        res = []
        for record in reads:
            name = record['name_prescriber_code']
            res.append((record['id'], name))
        return res
    
    def name_prescriber_code_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'prescriber_code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['prescriber_code']:
                name = name + ' (' + record['prescriber_code'] + ')'
            res.append((record['id'], name))
        return res

    def _name_prescriber_code_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_prescriber_code_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'partner': fields.many2one('res.partner', 'Related Partner', required=True,
                                   ondelete='cascade', help='Partner-related data of the prescriber'),
        #we need a related field in order to be able to sort the prescriber by name
        'name_related': fields.related('partner', 'name', type='char', string='Related Partner', 
                                       readonly=True, store=True),
        'alias' : fields.char('Alias', size=64, help='Common name that the Prescriber is referred'),
        'prescriber_code': fields.char(size=64, string='Prescriber Code', required=False),
        'name_prescriber_code': fields.function(_name_prescriber_code_get_fnc, type="char", string='Name (Prescriber Code)'),
        'prescriber_code2': fields.char(size=64, string='Prescriber Code2', required=False),
        'specialty_ids': fields.many2many('oehealth.specialty', 
                                          'oehealth_prescriber_specialty_rel', 
                                          'prescriber_id', 
                                          'specialty_id', 
                                          'Specialties'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_prescriber_tag_rel', 
                                    'prescriber_id', 
                                    'tag_id', 
                                    'Tags'),
        'prescriber_info': fields.text(string='Prescriber Info'),
        'prescriber_info2': fields.text(string='Prescriber Info-2'),
        'date_prescriber_inclusion' : fields.date('Inclusion Date'),
        'date_prescriber_activation' : fields.date('Activation Date'),
        'date_prescriber_inactivation' : fields.date('Inactivation Date'),
        'date_prescriber_suspension' : fields.date('Suspension Date'),
        'events_ids': fields.one2many('oehealth.event.participant',
                                      'prescriber_id',
                                      'Events'),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'prescriber_id',
                                          'Annotations'),
        # 'prescriber_status': fields.selection([
        #                                        ('U', 'Undefined'),
        #                                        ('A', 'Activated'),
        #                                        ('I', 'Inactivated'),
        #                                        ('S', 'Suspended'),
        #                                        ], string='Prescriber Status',
        #                                           select=True, sort=False, required=False, translate=True),
        'prescriber_status': fields.selection([('U', 'Undefined'),
                                               ('A', 'Activated'),
                                               ('I', 'Inactivated'),
                                               ('S', 'Suspended'),
                                               ], string='Prescriber Status', select=True, sort=False),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the prescriber without removing it."),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order='name_related'

    _sql_constraints = [('prescriber_code_uniq', 'unique(prescriber_code)', u'Duplicated Prescriber Code!'),
                        ('prescriber_code2_uniq', 'unique(prescriber_code2)', u'Duplicated Prescriber Code2!')]

    _defaults = {
        'active': 1,
        'customer': False,
        'supplier': False,
        'is_company': False,
        'is_health_partner': True,
        'is_prescriber': True,
        'prescriber_status': 'U',
        'state': 'new',
        'health_partner_code': '/',
        'prescriber_code2': '/',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'prescriber_code2' in vals or vals['prescriber_code2'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.prescriber.code')
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
                vals['prescriber_code2'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['prescriber_code2'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['prescriber_code2'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['prescriber_code2'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['prescriber_code2'] = code_str[14 - code_len:21]
        return super(oehealth_prescriber, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     prescribers_without_code = self.search(cr, uid, [('prescriber_code2', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(prescribers_without_code)
    #     super(oehealth_prescriber, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in prescribers_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.prescriber.code')
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
    #             vals['prescriber_code2'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['prescriber_code2'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['prescriber_code2'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['prescriber_code2'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['prescriber_code2'] = code_str[14 - code_len:21]
    #         super(oehealth_prescriber, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_prescriber_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_prescriber_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_prescriber_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_prescriber_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_prescriber()
