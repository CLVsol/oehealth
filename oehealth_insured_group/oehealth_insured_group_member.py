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

class oehealth_insured_group_member(osv.Model):
    _name = 'oehealth.insured.group.member'
    _columns = {
        'insured_group_id': fields.many2one('oehealth.insured.group', string='Insured Group',
                                            help='Insured Group Titular'),
        'insured_id': fields.many2one('oehealth.insured', string='Insured',
                                      help='Insured Group Member Name'),
        'role': fields.many2one('oehealth.insured.group.member.role', 'Role', required=True),
        'kinship': fields.many2one('oehealth.insured.group.member.kinship', 'Kinship', required=False),
        'info': fields.text(string='Info'),
        'tag_ids': fields.many2many('oehealth.tag', 
                                    'oehealth_insured_group_member_tag_rel', 
                                    'insured_group_member_id', 
                                    'tag_id', 
                                    'Tags'),
    }

oehealth_insured_group_member()
