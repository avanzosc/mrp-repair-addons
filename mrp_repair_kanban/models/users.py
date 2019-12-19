# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    pin_code = fields.Integer(string="PIN")
