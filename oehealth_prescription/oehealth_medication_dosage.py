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


class oehealth_medication_dosage(osv.Model):
    _name = 'oehealth.medication.dosage'

    _columns = {
        'abbreviation': fields.char(size=256, string='Abbreviation',
                                     help='Dosage abbreviation, such as tid in the US or tds in the UK'),
        'code': fields.char(size=8, string='Code',
                            help='Dosage Code,for example: SNOMED 229798009 = 3 times per day'),
        'name': fields.char(size=256, string='Frequency', required=True,
                            translate=True),
    }
    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),]

oehealth_medication_dosage()
