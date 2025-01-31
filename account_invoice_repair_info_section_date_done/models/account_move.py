# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_repair_name_for_values(self, repair):
        super_vals = super()._get_repair_name_for_values(repair)
        vals = _("%(super_vals)s, Date Done: %(date_done)s") % {
            "super_vals": super_vals,
            "date_done": repair.date_done.strftime("%d-%m-%Y") or "",
        }
        return vals
