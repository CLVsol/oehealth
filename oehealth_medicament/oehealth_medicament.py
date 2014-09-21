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

class oehealth_medicament(osv.Model):
    _name = 'oehealth.medicament'
    _description = "Medicament"
    _inherits={
               'product.product': 'product_id',
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
        reads = self.read(cr, uid, ids, ['name_active_component'], context=context)
        res = []
        for record in reads:
            name = record['name_active_component']
            res.append((record['id'], name))
        return res
    
    def name_active_component_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'active_component_name'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['active_component_name']:
                #name = name + ' (' + record['active_component'][1] + ')'
                name = name + ' (' + record['active_component_name'] + ')'
            res.append((record['id'], name))
        return res

    def _name_active_component_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_active_component_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True,
                                      ondelete='cascade', help='Product-related data of the medicament'),
        #we need a related field in order to be able to sort the medicament by name
        'name_product': fields.related('product_id', 'name', type='char', string='Related Product', 
                                       readonly=True, store=True),
        'medicament_category': fields.many2one('oehealth.medicament.category',
                                               'Medicament Category',select=True),
        'medicament_code': fields.char(size=64, string='Code', required=False),
        'medicament_name': fields.char(size=256, string='Name'),
        'active_component': fields.many2one('oehealth.medicament.active_component', string='Active Component', 
                                             help='Medicament Active Component'),
        'active_component_name': fields.related('active_component', 'name', type='char', string='Related Active Component', 
                                                readonly=True, store=True),
        'concentration': fields.char(size=256, string='Concentration'),
        'presentation': fields.char(size=256, string='Presentation'),
        'pres2': fields.integer(string='Presentation Quantity'),
        'pres3': fields.char(size=256, string='Presentation Form'),
        'composition': fields.text(string='Composition', help='Components'),
        'name_active_component': fields.function(_name_active_component_get_fnc, type="char", string='Name (Active Component)'),
        'indications': fields.text(string='Indication', help='Indications'),
        'therapeutic_action': fields.char(size=256,
                                          string='Therapeutic effect', 
                                          help='Therapeutic action'),
        'pregnancy_category': fields.selection([('A', 'A'),
                                                ('B', 'B'),
                                                ('C', 'C'),
                                                ('D', 'D'),
                                                ('X', 'X'),
                                                ('N', 'N'),
                                                ], string='Pregnancy Category', 
                                               help='** FDA Pregancy Categories ***\n'\
                                                    'CATEGORY A :Adequate and well-controlled human studies have failed'\
                                                    ' to demonstrate a risk to the fetus in the first trimester of'\
                                                    ' pregnancy (and there is no evidence of risk in later'\
                                                    ' trimesters).\n\n'\
                                                    'CATEGORY B : Animal reproduction studies have failed todemonstrate a'\
                                                    ' risk to the fetus and there are no adequate and well-controlled'\
                                                    ' studies in pregnant women OR Animal studies have shown an adverse'\
                                                    ' effect, but adequate and well-controlled studies in pregnant women'\
                                                    ' have failed to demonstrate a risk to the fetus in any'\
                                                    ' trimester.\n\n'
                                                    'CATEGORY C : Animal reproduction studies have shown an adverse'\
                                                    ' effect on the fetus and there are no adequate and well-controlled'\
                                                    ' studies in humans, but potential benefits may warrant use of the'\
                                                    ' drug in pregnant women despite potential risks. \n\n '\
                                                    'CATEGORY D : There is positive evidence of human fetal  risk based'\
                                                    ' on adverse reaction data from investigational or marketing'\
                                                    ' experience or studies in humans, but potential benefits may warrant'\
                                                    ' use of the drug in pregnant women despite potential risks.\n\n'\
                                                    'CATEGORY X : Studies in animals or humans have demonstrated fetal'\
                                                    ' abnormalities and/or there is positive evidence of human fetal risk'\
                                                    ' based on adverse reaction data from investigational or marketing'\
                                                    ' experience, and the risks involved in use of the drug in pregnant'\
                                                    ' women clearly outweigh potential benefits.\n\n'\
                                                    'CATEGORY N : Not yet classified'),
        'overdosage': fields.text(string='Overdosage', help='Overdosage'),
        'pregnancy_warning': fields.boolean(string='Pregnancy Warning', 
                                            help='The drug represents risk to pregnancy or lactancy'),
        'medicament_notes': fields.text(string='Medicament Info'),
        'storage': fields.text(string='Storage Conditions'),
        'adverse_reaction': fields.text(string='Adverse Reactions'),
        'dosage': fields.text(string='Dosage Instructions', 
                              help='Dosage / Indications'),
        'pregnancy': fields.text(string='Pregnancy and Lactancy', 
                                 help='Warnings for Pregnant Women'),
        'date_medicament_inclusion' : fields.date('Medicament Inclusion Date'),
        'date_medicament_activation' : fields.date('Medicament Activation Date'),
        'date_medicament_inactivation' : fields.date('Medicament Inactivation Date'),
        'date_medicament_suspension' : fields.date('Medicament Suspension Date'),
        'medicament_annotation_ids': fields.one2many('oehealth.annotation',
                                                     'medicament_id',
                                                     'Medicament Annotations'),
        'medicament_rgss': fields.selection([('U', 'Undefined'),
                                             ('R', 'Reference'),
                                             ('G', 'Generic'),
                                             ('S', 'Similar'),
                                             ], string='Medicament Status',
                                                  select=True, sort=False, required=False, translate=True),
        'medicament_tag_ids': fields.many2many('oehealth.tag', 
                                               'oehealth_medicament_tag_rel', 
                                               'medicament_id', 
                                               'tag_id', 
                                               'Tags'),
        # 'medicament_status': fields.selection([('U', 'Undefined'),
        #                                        ('A', 'Activated'),
        #                                        ('I', 'Inactivated'),
        #                                        ('S', 'Suspended'),
        #                                        ], string='Medicament Status',
        #                                           select=True, sort=False, required=False, translate=True),
        'medicament_status': fields.selection([('U', 'Undefined'),
                                               ('A', 'Activated'),
                                               ('I', 'Inactivated'),
                                               ('S', 'Suspended'),
                                               ], string='Medicament Status', select=True, sort=False),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'therapeutic_class': fields.many2one('oehealth.medicament.therapeutic_class', string='Therapeutic Class', 
                                             help='Medicament Therapeutic Class'),
        'manufacturer': fields.many2one('oehealth.medicament.manufacturer', string='Manufacturer', 
                                        help='Medicament Manufacturer'),
        'create_uid': fields.function(_compute_create_uid, method=True, type='char', string='Create User',),
        'create_date': fields.function(_compute_create_date, method=True, type='datetime', string='Create Date',),
        'write_uid': fields.function(_compute_write_uid, method=True, type='char', string='Write User',),
        'write_date': fields.function(_compute_write_date, method=True, type='datetime', string='Write Date',),
    }

    _order='name_product'

    _sql_constraints = [('medicament_code_uniq', 'unique(medicament_code)', u'Duplicated Medicament Code!')]

    _defaults = {
        'medicament_code': '/',
        'active': 1,
        'is_medicament': True,
        'medicament_status': 'U',
        'state': 'new',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not 'medicament_code' in vals or vals['medicament_code'] == '/':
            val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament.code')
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
                vals['medicament_code'] = code_str[18 - code_len:21]
            elif code_len > 3 and code_len <= 6:
                vals['medicament_code'] = code_str[17 - code_len:21]
            elif code_len > 6 and code_len <= 9:
                vals['medicament_code'] = code_str[16 - code_len:21]
            elif code_len > 9 and code_len <= 12:
                vals['medicament_code'] = code_str[15 - code_len:21]
            elif code_len > 12 and code_len <= 14:
                vals['medicament_code'] = code_str[14 - code_len:21]
        return super(oehealth_medicament, self).create(cr, uid, vals, context)

    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     medicaments_without_code = self.search(cr, uid, [('medicament_code', 'in', [False, '/']),('id', 'in', ids)], context=context)
    #     direct_write_ids = set(ids) - set(medicaments_without_code)
    #     super(oehealth_medicament, self).write(cr, uid, list(direct_write_ids), vals, context)
    #     for group_id in medicaments_without_code:
    #         val = self.pool.get('ir.sequence').get(cr, uid, 'oehealth.medicament.code')
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
    #             vals['medicament_code'] = code_str[18 - code_len:21]
    #         elif code_len > 3 and code_len <= 6:
    #             vals['medicament_code'] = code_str[17 - code_len:21]
    #         elif code_len > 6 and code_len <= 9:
    #             vals['medicament_code'] = code_str[16 - code_len:21]
    #         elif code_len > 9 and code_len <= 12:
    #             vals['medicament_code'] = code_str[15 - code_len:21]
    #         elif code_len > 12 and code_len <= 14:
    #             vals['medicament_code'] = code_str[14 - code_len:21]
    #         super(oehealth_medicament, self).write(cr, uid, group_id, vals, context)
    #     return True

    def oehealth_medicament_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_medicament_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_medicament_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_medicament_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_medicament()
