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

from openerp.osv import orm, fields

class oehealth_medicament_template(orm.Model):
    _inherit = 'oehealth.medicament.template'

    def _compute_total_refund_price(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            if r.refund_price:
                result[r.id] = r.refund_price * r.pack_quantity
            else:
                result[r.id] = 0.00
        return result

    _columns={
        'dispensation_id': fields.many2one('oehealth.dispensation',
                                            string='Dispensation ID', ),
        'pack_quantity': fields.integer(string='Pack Quantity',
                                        help='Quantity of packs of the medicament'),
        'refund_price': fields.float('Refund Price'),
        'total_refund_price' : fields.function(_compute_total_refund_price, method=True, type='float', size=32, string='Refund Value',),
    }
    
    _defaults = {
        'name': '/',
    }
    
oehealth_medicament_template()
