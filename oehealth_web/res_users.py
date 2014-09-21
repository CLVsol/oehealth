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

#from openerp.osv import orm, fields
from openerp.osv import fields, osv

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools

class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
        'disable_web_access': fields.boolean('Disable Web Access', help="Check to disable user web access."),
    }

    _defaults = {
        'disable_web_access': False,
    }

    def authenticate(self, db, login, password, user_agent_env):
        """Verifies and returns the user ID corresponding to the given
          ``login`` and ``password`` combination, or False if there was
          no matching user.

           :param str db: the database on which user is trying to authenticate
           :param str login: username
           :param str password: user password
           :param dict user_agent_env: environment dictionary describing any
               relevant environment attributes
        """
        uid = self.login(db, login, password)

        cr = pooler.get_db(db).cursor()
        try:
            cr.execute('SELECT disable_web_access FROM res_users WHERE id=%s', (uid,))
            if cr.rowcount:
                disable_web_access = cr.fetchone()[0]
                #print '------>', disable_web_access
                if disable_web_access == True:
                    return 0
        except Exception:
            _logger.exception("Failed to verify disable_web_access configuration parameter")
        finally:
            cr.close()


        if uid == openerp.SUPERUSER_ID:
            # Successfully logged in as admin!
            # Attempt to guess the web base url...
            if user_agent_env and user_agent_env.get('base_location'):
                cr = pooler.get_db(db).cursor()
                try:
                    base = user_agent_env['base_location']
                    ICP = self.pool.get('ir.config_parameter')
                    if not ICP.get_param(cr, uid, 'web.base.url.freeze'):
                        ICP.set_param(cr, uid, 'web.base.url', base)
                    cr.commit()
                except Exception:
                    _logger.exception("Failed to update web.base.url configuration parameter")
                finally:
                    cr.close()
        return uid


res_users()
