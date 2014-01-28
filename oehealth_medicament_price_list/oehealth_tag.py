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

class oehealth_tag(orm.Model):
    _inherit = 'oehealth.tag'

    _columns = {
        'medicament_price_list_ids': fields.many2many('oehealth.medicament.price_list', 
                                                      'oehealth_medicament_price_list_tag_rel', 
                                                      'tag_id', 
                                                      'price_list_id', 
                                                      'Medicament Catalogs'),
    }

oehealth_tag()
