# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    date_done = fields.Date(string="Date Done", copy=False)

    def action_repair_end(self):
        result = super(RepairOrder, self).action_repair_end()
        repairs = self.filtered(lambda x: x.state in ("done", "2binvoiced"))
        if repairs:
            repairs.write({"date_done": fields.Date.context_today(self)})
        return result
