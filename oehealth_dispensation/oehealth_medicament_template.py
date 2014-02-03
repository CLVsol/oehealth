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
            if r.state == 'authorized':
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
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}

        dispensation_id = vals['dispensation_id']
        dispensation_obj = self.pool.get('oehealth.dispensation')
        price_list_id = dispensation_obj.read(cr, uid, dispensation_id, ['price_list_id'])['price_list_id'][0]
        #vals['state_msg'] = price_list_id
        #vals['pack_quantity'] = dispensation_id

        medicament = vals['medicament']
        price_list_item_obj = self.pool.get('oehealth.medicament.price_list.item')
        item_id = price_list_item_obj.search(cr, uid, [('price_list_id', '=', price_list_id),('medicament_id', '=', medicament),])
        if item_id != []:
            refund_price = price_list_item_obj.read(cr, uid, item_id, ['refund_price'])[0]['refund_price']
        else:
            refund_price = 0.00

        vals['refund_price'] = refund_price

        return super(oehealth_medicament_template, self).create(cr, uid, vals, context)

oehealth_medicament_template()
