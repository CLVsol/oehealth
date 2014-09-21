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

class oehealth_lab_test_criterion(osv.osv):
    _name = "oehealth.lab_test.criterion"
    _description = "Lab Test Criterion"    
    _columns ={
       'name' : fields.char('Test', size=64),
       'result' : fields.text('Result'),
       'normal_range' : fields.text('Normal Range'),
       'outcome_ids': fields.many2many('oehealth.lab_test.outcome', 
                                       'oehealth_lab_test_outcome_rel', 
                                       'criterion_id', 
                                       'outcome_id', 
                                       'Outcomes'),
       'valid_values' : fields.text('Valid Values'),
       'unit' : fields.many2one('oehealth.lab_test.unit', 'Units'),
       'lab_test_type_id' : fields.many2one('oehealth.lab_test.type','Test type'),
       'lab_test_id' : fields.many2one('oehealth.lab_test','Test Cases'),
       'sequence' : fields.integer('Sequence'),       
       }
    _defaults = {
         'sequence' : lambda *a : 1,        
         }
    _order="sequence"

oehealth_lab_test_criterion()
