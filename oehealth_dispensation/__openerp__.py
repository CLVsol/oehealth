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

{
    'name': 'OpenERP Health: Dispensation',
    'version': '1.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'http://oehealth.org',
    'description': '''
    ''',
    'images': [],
    'depends': ['oehealth_annotation',
                'oehealth_tag',
                'oehealth_medicament',
                'oehealth_prescriber',
                'oehealth_pharmacy',
                'oehealth_insured_card',
                'oehealth_prescription_transcription',
                ],
    'data': ['security/ir.model.access.csv',
             ],
    'demo': [],
    'test': [],
    'init_xml': ['security/oehealth_dispensation_security.xml',
                 'oehealth_dispensation_view.xml',
                 'oehealth_dispensation_category_view.xml',
                 'oehealth_dispensation_workflow.xml',
                 'oehealth_medicament_template_view.xml',
                 'wizard/create_lab_test.xml'
                 ],
    'test': [],
    'update_xml': ['oehealth_dispensation_sequence.xml'
                   ],
    'installable': True,
    'active': False,
    'css': [],
}
