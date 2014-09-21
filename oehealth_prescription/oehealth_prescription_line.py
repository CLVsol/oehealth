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


class oehealth_prescription_line(osv.Model):
    _name = 'oehealth.prescription.line'

    _columns = {
        'refills': fields.integer(string='Refills #'),
        'prescription_order_id': fields.many2one('oehealth.prescription.order',
                                                 string='Prescription ID', ),
        'allow_substitution': fields.boolean(string='Allow substitution'),
        'prnt': fields.boolean(string='Print',
                               help='Check this box to print this line of the prescription.'),
        'review': fields.datetime(string='Review'),
        'short_comment': fields.char(size=256, string='Comment',
                                     help='Short comment on the specific drug'),
        'template': fields.many2one('oehealth.medication.template',
                                    string='Medication Template', ),
        'quantity': fields.integer(string='Quantity'),
    }

oehealth_prescription_line()
