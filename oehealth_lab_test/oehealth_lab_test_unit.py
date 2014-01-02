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

from osv import fields, osv

class oehealth_lab_test_unit(osv.osv):
    _name = "oehealth.lab_test.unit"
    _columns = {
        'name' : fields.char('Unit', size=25),
        'code' : fields.char('Code', size=25),
        'info' : fields.text ('Description'),
        }
    _sql_constraints = [('name_uniq', 'unique(name)', 'The Unit name must be unique'),
                        ('code_uniq', 'unique(code)', 'The Unit code must be unique')
                        ]
    
oehealth_lab_test_unit()
