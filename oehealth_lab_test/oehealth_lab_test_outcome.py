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


class oehealth_lab_test_outcome(osv.osv):
    _name = 'oehealth.lab_test.outcome'
    _description = 'Lab Test Outcomes'

    _columns = {
        'name': fields.char('Lab Test Outcome', required=True, size=64, translate=True),
        'description': fields.text(string='Description'),
        'info': fields.text(string='Info'),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the outcome without removing it."),
    }

    _defaults = {
        'active': 1,
    }

    _order = 'name'

oehealth_lab_test_outcome()
