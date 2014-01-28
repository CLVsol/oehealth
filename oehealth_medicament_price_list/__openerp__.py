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
    'name': 'OpenERP Health: Medicament Price List',
    'version': '1.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'http://oehealth.org',
    'description': '''
    ''',
    'images': [],
    'depends': ['oehealth_base',
                'oehealth_annotation',
                'oehealth_tag',
                'oehealth_medicament',
                ],
    'data': ['security/ir.model.access.csv',
             ],
    'demo': [],
    'test': [],
    'init_xml': ['security/oehealth_medicament_price_list_security.xml',
                 'oehealth_annotation_view.xml',
                 'oehealth_medicament_price_list_category_view.xml',
                 'oehealth_medicament_price_list_workflow.xml',
                 'oehealth_medicament_price_list_view.xml',
                 'oehealth_medicament_price_list_sequence.xml',
                 'oehealth_tag_view.xml',
                 'oehealth_medicament_price_list_item_view.xml',
                  ],
    'test': [],
    'update_xml': [],
    'installable': True,
    'active': False,
    'css': [],
}
