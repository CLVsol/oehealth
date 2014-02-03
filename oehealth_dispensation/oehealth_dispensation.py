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
import time

class oehealth_dispensation(osv.Model):
    _name='oehealth.dispensation'

    def _compute_total_refund_price(self, cr, uid, ids, field_name, arg, context={}):
        total = {}
        for obj in self.browse(cr, uid, ids, context=context):
            total[obj.id] = sum(o2m.total_refund_price for o2m in obj.dispensation_line)
        return total

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

    _columns={
        'name': fields.char(size=256, string='Dispensation ID', required=True,
                            help='Type in the ID of this dispensation'),
        'dispensation_date': fields.date(string='Dispensation Date', required=True),
        'prescription_date': fields.date(string='Prescription Date', required=True),
        'prescriber_id': fields.many2one('oehealth.prescriber', string='Prescriber', required=True),
        'pharmacy_id': fields.many2one('oehealth.pharmacy', string='Pharmacy', required=True),
        'insured_card_id': fields.many2one('oehealth.insured.card', string='Insured Card', required=True),
        'price_list_id': fields.many2one('oehealth.medicament.price_list', string='Price List', required=True),
        #'patient_id': fields.many2one('oehealth.patient', string='Patient', required=True),
        #'pregnancy_warning': fields.boolean(string='Pregancy Warning', readonly=True),
        'transcription_id': fields.many2one('oehealth.prescription.transcription', string='Transcription ID', required=False),
        'category_ids': fields.many2many('oehealth.dispensation.category', 
                                         'oehealth_dispensation_category_rel', 
                                         'dispensation_id', 
                                         'category_id', 
                                         'Categories'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_dispensation_tag_rel', 
                                    'dispensation_id', 
                                    'tag_id', 
                                    'Tags'),
        'notes': fields.text(string='Dispensation Notes'),
        #'prescription_line': fields.one2many('oehealth.dispensation.line',
        #                                     'pbm_prescription_order_id',
        #                                     string='Dispensation line',),
        'dispensation_line': fields.one2many('oehealth.medicament.template',
                                             'dispensation_id',
                                             string='Dispensation lines',),
        #'pbm_prescription_warning_ack': fields.boolean(string='Dispensation verified'),
        #'user_id': fields.many2one('res.users', string='Prescribing Doctor', required=True),
        'active': fields.boolean('Active', help="The active field allows you to hide the dispensation without removing it."),
        'annotation_ids': fields.one2many('oehealth.annotation',
                                          'dispensation_id',
                                          'Annotations'),
        'total_refund' : fields.function(_compute_total_refund_price, method=True, type='float', size=32, string='Dispensation Total Refund',),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
        }
    
    _sql_constraints = [
                        ('uniq_name', 'unique(name)', "The Dispensation ID must be unique!"),
                        ]

    _defaults={
        'name': '/',
        'dispensation_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'active': 1,
        'state': 'new',
        }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'name' in vals or vals['name'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.dispensation.code')
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
        return super(oehealth_dispensation, self).create(cr, uid, vals, context)

    def oehealth_dispensation_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_dispensation_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_dispensation_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_dispensation_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

    def create_transcription(self, cr, uid, ids, context={}):
        data=ids

        test_request_obj = self.pool.get('oehealth.dispensation')
        lab_obj = self.pool.get('oehealth.dispensation')

        test_report_data={}
        test_cases = []
        test_obj = test_request_obj.browse(cr, uid, context.get('active_id'), context=context)
        #if test_obj.state == 'tested':
        if test_obj.state != 'tested':
            #raise  osv.except_osv(_('UserError'),_('Test Report already created.'))
            raise  osv.except_osv(('UserError'),('Test Report already created.'))
        test_report_data['test'] = test_obj.name.id
        test_report_data['patient'] = test_obj.patient_id.id
        #test_report_data['requestor'] = test_obj.doctor_id.id
        test_report_data['date_requested'] = test_obj.date
        
        for criterion in test_obj.name.criteria:
            test_cases.append((0,0,{'name':criterion.name,
                                    'sequence':criterion.sequence,
                                    'normal_range':criterion.normal_range,
                                    'unit':criterion.unit.id,
                                    }))
        test_report_data['criteria'] = test_cases
        lab_id = lab_obj.create(cr,uid,test_report_data,context=context)
        test_request_obj.write(cr, uid, context.get('active_id'), {'state':'tested'})
        return {
                'domain': "[('id','=', "+str(lab_id)+")]",
                'name': 'Lab Test Report',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'oehealth.lab_test',
                'type': 'ir.actions.act_window'
        }
        
    def get_authorization(self, cr, uid, ids, context={}):
        
        data=ids

        test_request_obj = self.pool.get('oehealth.dispensation')
        lab_obj = self.pool.get('oehealth.dispensation')

        test_report_data={}
        test_cases = []
        test_obj = test_request_obj.browse(cr, uid, context.get('active_id'), context=context)
        #if test_obj.state == 'tested':
        if test_obj.state != 'tested':
            #raise  osv.except_osv(_('UserError'),_('Test Report already created.'))
            raise  osv.except_osv(('UserError'),('Test Report already created.'))
        test_report_data['test'] = test_obj.name.id
        test_report_data['patient'] = test_obj.patient_id.id
        #test_report_data['requestor'] = test_obj.doctor_id.id
        test_report_data['date_requested'] = test_obj.date
        
        for criterion in test_obj.name.criteria:
            test_cases.append((0,0,{'name':criterion.name,
                                    'sequence':criterion.sequence,
                                    'normal_range':criterion.normal_range,
                                    'unit':criterion.unit.id,
                                    }))
        test_report_data['criteria'] = test_cases
        lab_id = lab_obj.create(cr,uid,test_report_data,context=context)
        test_request_obj.write(cr, uid, context.get('active_id'), {'state':'tested'})
        return {
                'domain': "[('id','=', "+str(lab_id)+")]",
                'name': 'Lab Test Report',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'oehealth.lab_test',
                'type': 'ir.actions.act_window'
        }

oehealth_dispensation()
