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
    'name': 'OpenERP Health: Community',
    'version': '1.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'http://oehealth.org',
    'description': '''
    ''',
    'images': [],
    'depends': ['oehealth_person',
                'oehealth_family',
                ],
    'data': ['security/ir.model.access.csv',
             ],
    'demo': [],
    'test': [],
    'init_xml': ['res_partner_view.xml',
                 'oehealth_annotation_view.xml',
                 'security/oehealth_community_security.xml',
                 'oehealth_community_workflow.xml',
                 'oehealth_community_view.xml',
                 'oehealth_community_category_view.xml',
                 'oehealth_comunity_person_member_view.xml',
                 'oehealth_comunity_family_member_view.xml',
                 'oehealth_person_view.xml',
                 'oehealth_family_view.xml',
                 'oehealth_tag_view.xml',
                  ],
    'test': [],
    'update_xml': ['oehealth_community_sequence.xml'],
    'installable': True,
    'active': False,
    'css': [],
}
