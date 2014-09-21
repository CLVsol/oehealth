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

class oehealth_medication(osv.Model):
    _name = 'oehealth.medication'
    _description = "Medication"

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
        reads = self.read(cr, uid, ids, ['name', 'active_component'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['active_component']:
                #name = name + ' (' + record['active_component'][1] + ')'
                name = name + ' (' + record['active_component'] + ')'
            res.append((record['id'], name))
        return res

    def _name_active_component_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_active_component_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name' : fields.char ('Name', size=128, help="Medication Name"),
        'medication_code': fields.char(size=64, string='Medication Code', required=False),
        'active_component': fields.char(size=256, string='Active component',
                                        translate=False, help='Active Component'),
        #'form': fields.many2one('oehealth.drug.form', string='Form', 
        #                         help='Medication form, such as tablet or gel'),
        'presentation': fields.text(string='Presentation'),
        'name_active_component': fields.function(_name_active_component_get_fnc, type="char", string='Name (Active Component)'),
        'composition': fields.text(string='Composition', help='Components'),
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
        #'storage': fields.text(string='Storage Conditions'),
        'adverse_reaction': fields.text(string='Adverse Reactions'),
        'dosage': fields.text(string='Dosage Instructions', 
                              help='Dosage / Indications'),
        'pregnancy': fields.text(string='Pregnancy and Lactancy', 
                                 help='Warnings for Pregnant Women'),
        'medication_info': fields.text(string='Medication Info'),
        #'medication_annotation_ids': fields.one2many('oehealth.annotation',
        #                                             'medication_id',
        #                                             'Medication Annotations'),
        #'category': fields.many2one('oehealth.medication.category',
        #                            'Category',select=True),
        #'medication_category_ids': fields.many2many('oehealth.medication.category', 
        #                                            'oehealth_medication_category_rel', 
        #                                            'medication_id', 
        #                                            'category_id', 
        #                                            'Medication Categories'),
        'medication_tag_ids': fields.many2many('oehealth.tag', 
                                               'oehealth_medication_tag_rel', 
                                               'medication_id', 
                                               'tag_id', 
                                               'Medication Tags'),
        'state': fields.selection([('new','New'),
                                   ('revised','Revised'),
                                   ('waiting','Waiting'),
                                   ('okay','Okay')], 'Stage', readonly=True),
        'active': fields.boolean('Active', help="The active field allows you to hide the medication without removing it."),
    }

    _order='name'

    _sql_constraints = [('medication_code_uniq', 'unique(medication_code)', u'Duplicated Medication Code!')]

    _defaults = {
        'active': 1,
        'state': 'new',
    }
    
    def oehealth_medication_new(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'new'})
         return True

    def oehealth_medication_revised(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'revised'})
         return True

    def oehealth_medication_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'waiting'})
         return True

    def oehealth_medication_okay(self, cr, uid, ids):
         self.write(cr, uid, ids, {'state': 'okay'})
         return True

oehealth_medication()
