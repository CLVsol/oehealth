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

class oehealth_family_member(osv.Model):
    _name = 'oehealth.family.member'
    _columns = {
        'family_id': fields.many2one('oehealth.family', string='Family',
                                     help='Family code'),
        'person_id': fields.many2one('oehealth.person', string='Person',
                                     help='Family Member Name'),
        'role': fields.many2one('oehealth.family.member.role', 'Role', required=True),
        'info': fields.text(string='Info'),
    }

oehealth_family_member()
