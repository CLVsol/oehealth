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

class oehealth_lab_test_type (osv.osv):
    _name = "oehealth.lab_test.type"
    _description = "Type of Lab test"
    _columns = {
        'name' : fields.char ('Test',size=128,help="Test type, eg X-Ray, hemogram, biopsy..."),
        'code' : fields.char ('Code',size=32,help="Short name - code for the test"),
        'info' : fields.text ('Description'),
        'product_id' : fields.many2one('product.product', 'Service', required=True),
        'criteria': fields.one2many('oehealth.lab_test.criterion','lab_test_type_id','Test Cases'),
    }
    _sql_constraints = [('name_uniq', 'unique (name)', 'The Lab Test name must be unique'),
                        ('code_uniq', 'unique (code)', 'The Lab Test code must be unique')
                        ]

oehealth_lab_test_type()