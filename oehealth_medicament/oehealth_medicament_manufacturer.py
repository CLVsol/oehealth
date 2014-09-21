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


class oehealth_medicament_manufacturer(osv.osv):
    _name = 'oehealth.medicament.manufacturer'
    _description = 'Medicament Manufacturer'

    _columns = {
        'name': fields.char(size=256, string='Manufacturer', required=True),
        'code': fields.char(size=256, string='Code'),
        'info': fields.text(string='Info'),
        'active': fields.boolean('Active', help="The active field allows you to hide the manufacturer without removing it."),
    }
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
        ('code_uniq', 'UNIQUE(code)', 'Code must be unique!'),
    ]

oehealth_medicament_manufacturer()
